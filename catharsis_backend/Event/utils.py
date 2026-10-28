"""
    Logique métier de l'app analytics.
    Les vues se contentent de valider la requête, d'appeler une fonction d'ici
    et de renvoyer la Response.
"""
from calendar import monthrange
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, time, timedelta
from pathlib import Path
import re
from urllib.parse import urlparse

from django.conf import settings
from django.db import transaction
from django.db.models import Case, Count, IntegerField, Value, When
from django.db.models.functions import ExtractDay, ExtractHour, ExtractMonth, ExtractWeekDay
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.exceptions import APIException, NotFound, ValidationError

from .models import Event, Project, Session

# --------------------------------------------------------------------------- #
# Constantes
# --------------------------------------------------------------------------- #
PERIODS = ('day', 'month', 'year')
DEFAULT_PERIOD = 'month'

AUDIENCE_DIMENSIONS = {
    'countries', 'sources', 'devices', 'browsers', 'operating-systems', 'pages',
}
UNKNOWN = 'Inconnu'
UNKNOWN_COUNTRY = 'Pays inconnu'
DIRECT_SOURCE = 'Accès direct / inconnu'
GEOIP_NOT_CONFIGURED = (
    'Configurez GEOIP_COUNTRY_DB avec le chemin de votre base '
    'locale GeoLite2-Country.mmdb pour afficher les pays.'
)

HEATMAP_DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
HEATMAP_HOURS = [
    '12 am', '2 am', '4 am', '6 am', '8 am', '10 am',
    '12 pm', '2 pm', '4 pm', '6 pm', '8 pm', '10 pm',
]

DEVICE_STYLE = {  # clé -> (nom dashboard, couleur)
    'desktop': ('Desktop', '#2563eb'),
    'mobile': ('Mobile', '#38bdf8'),
    'tablet': ('Tablet', '#94a3b8'),
}
DEVICE_LABELS_FR = {'desktop': 'Ordinateur', 'mobile': 'Mobile', 'tablet': 'Tablette'}

BROWSER_RULES = (
    (('edg/',), 'Microsoft Edge'),
    (('opr/', 'opera'), 'Opera'),
    (('firefox/',), 'Firefox'),
    (('chrome/', 'crios/'), 'Google Chrome'),
    (('safari/',), 'Safari'),
)
OS_RULES = (
    (('windows',), 'Windows'),
    (('android',), 'Android'),
    (('iphone', 'ipad', 'ios'), 'iOS'),
    (('mac os', 'macintosh'), 'macOS'),
    (('linux',), 'Linux'),
)

MONTH_LABELS = ('Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc')
MONTH_NAMES_FR = (
    'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
    'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre',
)


class GeoIPDatabaseMissing(APIException):
    status_code = 503
    default_detail = 'La base GeoIP locale configurée est introuvable.'
    default_code = 'geoip_database_missing'


# --------------------------------------------------------------------------- #
# Helpers génériques
# --------------------------------------------------------------------------- #
def format_number(value, sep=' '):
    return f"{value:,}".replace(',', sep)


def normalize_period(raw):
    period = (raw or DEFAULT_PERIOD).lower()
    return period if period in PERIODS else DEFAULT_PERIOD


def parse_audience_date_range(raw_start, raw_end):
    """Validate the optional, all-or-nothing date range used by audience reports."""
    if not raw_start and not raw_end:
        return None, None
    if not raw_start or not raw_end:
        raise ValidationError({'date_range': 'start_date et end_date doivent être fournis ensemble.'})

    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not date_pattern.fullmatch(raw_start) or not date_pattern.fullmatch(raw_end):
        raise ValidationError({'date_range': 'Les dates doivent respecter le format YYYY-MM-DD.'})

    try:
        start_date, end_date = parse_date(raw_start), parse_date(raw_end)
    except ValueError as error:
        raise ValidationError({'date_range': 'Une ou plusieurs dates sont invalides.'}) from error
    if start_date is None or end_date is None:
        raise ValidationError({'date_range': 'Une ou plusieurs dates sont invalides.'})
    if start_date > end_date:
        raise ValidationError({'date_range': 'start_date doit précéder ou égaler end_date.'})
    return start_date, end_date


def get_user_projects(user, site_id=None):
    """Projets de l'utilisateur, éventuellement restreints à un site_id."""
    projects = Project.objects.filter(customer=user)
    if site_id:
        projects = projects.filter(site_id=site_id)
        if not projects.exists():
            raise NotFound('Site introuvable.')
    return projects


def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


# --------------------------------------------------------------------------- #
# Détection appareil / navigateur / OS
# --------------------------------------------------------------------------- #
def detect_device(user_agent):
    agent = (user_agent or '').lower()
    if 'ipad' in agent or 'tablet' in agent:
        return 'tablet'
    if any(token in agent for token in ('mobile', 'android', 'iphone')):
        return 'mobile'
    return 'desktop'


def _first_match(user_agent, rules):
    agent = (user_agent or '').lower()
    for needles, label in rules:
        if any(needle in agent for needle in needles):
            return label
    return UNKNOWN


def detect_browser(user_agent):
    return _first_match(user_agent, BROWSER_RULES)


def detect_os(user_agent):
    return _first_match(user_agent, OS_RULES)


# --------------------------------------------------------------------------- #
# Collecte d'un événement
# --------------------------------------------------------------------------- #
@transaction.atomic
def record_event(serializer, request):
    """Enregistre l'événement et rattache (ou crée) la session correspondante."""
    data = serializer.validated_data
    project = Project.objects.filter(site_id=data['site_id']).first()
    if project is None:
        raise ValidationError({'site_id': 'Site inconnu.'})

    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    Session.objects.get_or_create(
        project=project,
        session_id=data['session_id'],
        defaults={'ip_address': ip, 'user_agent': user_agent},
    )
    return serializer.save(ip_address=ip, user_agent=user_agent)


# --------------------------------------------------------------------------- #
# Dashboard
# --------------------------------------------------------------------------- #
def build_dashboard(projects, period):
    site_ids = list(projects.values_list('site_id', flat=True))
    now = timezone.localtime()
    start_date, previous_start, previous_end = _dashboard_period_bounds(period, now)

    sessions = Session.objects.filter(
        project__in=projects,
        started_at__gte=start_date,
        started_at__lt=now,
    )
    previous_sessions = Session.objects.filter(
        project__in=projects,
        started_at__gte=previous_start,
        started_at__lt=previous_end,
    )
    events = Event.objects.filter(
        site_id__in=site_ids,
        client_timestamp__gte=start_date,
        client_timestamp__lt=now,
    )

    total_sessions = sessions.count()
    visitors = sessions.values('project_id', 'session_id').distinct().count()
    previous_total_sessions = previous_sessions.count()
    previous_visitors = previous_sessions.values('project_id', 'session_id').distinct().count()

    return {
        'site_id': site_ids[0] if site_ids else None,
        'kpi': _kpis(visitors, total_sessions, previous_visitors, previous_total_sessions),
        'heatmap': {
            'days': HEATMAP_DAYS,
            'hours': HEATMAP_HOURS,
            'matrix': _heatmap(events),
        },
        'active_users': _timeline(sessions, period, start_date),
        'devices': _device_breakdown(sessions, visitors),
    }


def _dashboard_period_bounds(period, now):
    if period == 'day':
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        previous_start = start - timedelta(days=1)
        previous_end = previous_start + (now - start)
    elif period == 'year':
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        previous_start = start.replace(year=start.year - 1)
        previous_end = min(previous_start + (now - start), start)
    else:
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        previous_start = (start - timedelta(days=1)).replace(day=1)
        previous_end = min(previous_start + (now - start), start)
    return start, previous_start, previous_end


def _percentage_change(current, previous):
    if previous == 0:
        return (0.0, 'Nouvelle période') if current else (0.0, 'Aucune donnée')
    return round((current - previous) / previous * 100, 1), 'vs période précédente'


def _kpis(visitors, sessions, previous_visitors, previous_sessions):
    def kpi(value, formatted, previous_value):
        trend, trend_period = _percentage_change(value, previous_value)
        return {
            'value': value,
            'formatted': formatted,
            'trend': trend,
            'is_positive': value >= previous_value,
            'period': trend_period,
        }

    return {
        'users': kpi(visitors, format_number(visitors), previous_visitors),
        'revenue': {
            'value': 0.0,
            'formatted': '—',
            'trend': 0.0,
            'is_positive': True,
            'period': 'Non suivi',
        },
        'conversion_rate': {
            'value': 0.0,
            'formatted': '—',
            'trend': 0.0,
            'is_positive': True,
            'period': 'Non suivi',
        },
        'sessions': kpi(sessions, format_number(sessions, '.'), previous_sessions),
    }


def _heatmap(events):
    """Matrice 7 jours x 12 créneaux de 2 h, calculée côté base de données."""
    matrix = [[0] * len(HEATMAP_HOURS) for _ in HEATMAP_DAYS]
    rows = (
        events.order_by()
        .annotate(
            weekday=ExtractWeekDay('client_timestamp'),  # 1 = dimanche
            hour=ExtractHour('client_timestamp'),
        )
        .values('weekday', 'hour')
        .annotate(total=Count('id'))
    )
    for row in rows:
        matrix[row['weekday'] - 1][row['hour'] // 2] += row['total']
    return matrix


def _timeline(sessions, period, start_date):
    if period == 'day':
        labels = [f'{hour:02d}h' for hour in range(0, 24, 4)]
        hour = ExtractHour('started_at', tzinfo=timezone.get_current_timezone())
        rows = (
            sessions.annotate(hour=hour)
            .annotate(bucket=Case(
                When(hour__lt=4, then=Value(0)),
                When(hour__lt=8, then=Value(1)),
                When(hour__lt=12, then=Value(2)),
                When(hour__lt=16, then=Value(3)),
                When(hour__lt=20, then=Value(4)),
                default=Value(5),
                output_field=IntegerField(),
            ))
            .values('bucket')
            .annotate(total=Count('id'))
        )
        data = [0] * len(labels)
        for row in rows:
            data[row['bucket']] = row['total']
        peak_labels = [f"Aujourd'hui · {label}" for label in labels]
    elif period == 'year':
        labels = list(MONTH_LABELS)
        rows = (
            sessions.annotate(bucket=ExtractMonth('started_at', tzinfo=timezone.get_current_timezone()))
            .values('bucket')
            .annotate(total=Count('id'))
        )
        data = [0] * 12
        for row in rows:
            data[row['bucket'] - 1] = row['total']
        peak_labels = [f'{label} {start_date.year}' for label in labels]
    else:
        day_count = monthrange(start_date.year, start_date.month)[1]
        labels = [str(day) for day in range(1, day_count + 1)]
        rows = (
            sessions.annotate(bucket=ExtractDay('started_at', tzinfo=timezone.get_current_timezone()))
            .values('bucket')
            .annotate(total=Count('id'))
        )
        data = [0] * day_count
        for row in rows:
            data[row['bucket'] - 1] = row['total']
        peak_labels = [
            f"{day} {MONTH_NAMES_FR[start_date.month - 1]}" for day in range(1, day_count + 1)
        ]

    peak_index = max(range(len(data)), key=data.__getitem__)
    peak_label = peak_labels[peak_index] if data[peak_index] else 'Pas de données'
    return {
        'period': period,
        'peak_value': max(data),
        'peak_label': peak_label,
        'labels': labels,
        'data': data,
    }


def _device_breakdown(sessions, visitors):
    counts = Counter()
    rows = sessions.order_by().values('user_agent').annotate(n=Count('id'))
    for row in rows:
        counts[detect_device(row['user_agent'])] += row['n']

    total = sum(counts.values())
    pct = {key: round(counts[key] / total * 100, 1) if total else 0.0 for key in DEVICE_STYLE}
    if total:  # la tablette absorbe l'arrondi pour garder 100 %
        pct['tablet'] = round(max(0.0, 100.0 - pct['desktop'] - pct['mobile']), 1)

    return {
        'total_visitors': visitors,
        'formatted_total': format_number(visitors, '.'),
        'breakdown': [
            {'name': name, 'percentage': pct[key], 'count': counts[key], 'color': color}
            for key, (name, color) in DEVICE_STYLE.items()
        ],
    }


# --------------------------------------------------------------------------- #
# Rapport d'audience
# --------------------------------------------------------------------------- #
def _safe_hostname(url):
    try:
        return urlparse(url).hostname if url else None
    except ValueError:
        return None


def _safe_path(url):
    try:
        return urlparse(url).path or '/'
    except ValueError:
        return '/'


LABEL_RESOLVERS = {
    'sources': lambda e: _safe_hostname((e['properties'] or {}).get('referrer')) or DIRECT_SOURCE,
    'devices': lambda e: DEVICE_LABELS_FR[detect_device(e['user_agent'])],
    'browsers': lambda e: detect_browser(e['user_agent']),
    'operating-systems': lambda e: detect_os(e['user_agent']),
    'pages': lambda e: _safe_path(e['url']),
}


@contextmanager
def _country_resolver(database_path):
    if not Path(database_path).is_file():
        raise GeoIPDatabaseMissing()

    from geoip2.database import Reader  # import paresseux : dépendance optionnelle
    from geoip2.errors import AddressNotFoundError

    with Reader(database_path) as reader:
        def resolve(event):
            if not event['ip_address']:
                return UNKNOWN_COUNTRY
            try:
                return reader.country(event['ip_address']).country.name or UNKNOWN_COUNTRY
            except AddressNotFoundError:
                return UNKNOWN_COUNTRY
        yield resolve


def _group_sources(events):
    """Pour chaque session, attribue sa source d'acquisition (le premier référent externe, sinon direct)."""
    session_sources = {}
    visitors = set()
    for event in events.iterator():
        key = (event['site_id'], event['session_id'])
        visitors.add(key)
        referrer = (event['properties'] or {}).get('referrer')
        hostname = _safe_hostname(referrer)
        if hostname and key not in session_sources:
            session_sources[key] = hostname

    groups = {}
    for key in visitors:
        source = session_sources.get(key, DIRECT_SOURCE)
        groups.setdefault(source, set()).add(key)
    return groups, len(visitors)


def _group_sessions(events, resolver=None):
    """Retourne ({label: {sessions}}, nombre total de visiteurs) en un seul passage."""
    groups, visitors = {}, set()
    for event in events.iterator():
        key = (event['site_id'], event['session_id'])
        visitors.add(key)
        if resolver:
            groups.setdefault(resolver(event), set()).add(key)
    return groups, len(visitors)


def build_audience_report(projects, dimension, start_date=None, end_date=None):
    if dimension not in AUDIENCE_DIMENSIONS:
        raise ValidationError({'dimension': 'Dimension invalide.'})

    event_queryset = Event.objects.filter(site_id__in=projects.values_list('site_id', flat=True))
    if start_date is not None and end_date is not None:
        start_at = timezone.make_aware(datetime.combine(start_date, time.min))
        end_at = timezone.make_aware(datetime.combine(end_date + timedelta(days=1), time.min))
        event_queryset = event_queryset.filter(
            client_timestamp__gte=start_at,
            client_timestamp__lt=end_at,
        )
    events = event_queryset.order_by().values(
        'site_id', 'session_id', 'ip_address', 'user_agent', 'url', 'properties',
    )

    available, message = True, ''
    if dimension == 'countries':
        database_path = getattr(settings, 'GEOIP_COUNTRY_DB', None)
        if database_path:
            with _country_resolver(database_path) as resolver:
                groups, total = _group_sessions(events, resolver)
        else:
            available, message = False, GEOIP_NOT_CONFIGURED
            groups, total = _group_sessions(events)
    elif dimension == 'sources':
        groups, total = _group_sources(events)
    else:
        groups, total = _group_sessions(events, LABEL_RESOLVERS[dimension])

    rows = sorted(
        ({'label': label, 'visitors': len(keys)} for label, keys in groups.items()),
        key=lambda row: (-row['visitors'], row['label'].casefold()),
    )
    return {
        'dimension': dimension,
        'available': available,
        'message': message,
        'total_visitors': total,
        'results': rows[:100],
    }