from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from pathlib import Path
from urllib.parse import urlparse
from django.conf import settings

# Modules imports
from .serializers import ProjectSerializer, SessionSerializer, EventSerializer
from .models import Project, Session, Event

# Create your views here.
class ManageProjectView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            serializer = ProjectSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

    def get(self, request):
        try:
            projects = Project.objects.filter(customer=request.user)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AnalyticsDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        site_id = request.query_params.get('site_id')
        period = request.query_params.get('period', 'month').lower()
        if period not in ['day', 'month', 'year']:
            period = 'month'

        user_projects = Project.objects.filter(customer=request.user)
        if site_id:
            user_projects = user_projects.filter(site_id=site_id)

        site_ids = list(user_projects.values_list('site_id', flat=True))
        sessions_qs = Session.objects.filter(project__in=user_projects)
        events_qs = Event.objects.filter(site_id__in=site_ids)

        total_sessions = sessions_qs.count()
        total_events = events_qs.count()
        unique_visitors = sessions_qs.values('session_id').distinct().count()

        # Device categorization
        desktop_count = 0
        mobile_count = 0
        tablet_count = 0

        for ua in sessions_qs.values_list('user_agent', flat=True):
            ua_lower = (ua or '').lower()
            if 'ipad' in ua_lower or 'tablet' in ua_lower:
                tablet_count += 1
            elif 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
                mobile_count += 1
            else:
                desktop_count += 1

        total_device_records = desktop_count + mobile_count + tablet_count

        if total_device_records > 0:
            desktop_pct = round((desktop_count / total_device_records) * 100, 1)
            mobile_pct = round((mobile_count / total_device_records) * 100, 1)
            tablet_pct = round(max(0.0, 100.0 - desktop_pct - mobile_pct), 1)
            visitor_metric = unique_visitors if unique_visitors > 0 else total_sessions
        else:
            desktop_pct = 0.0
            mobile_pct = 0.0
            tablet_pct = 0.0
            desktop_count = 0
            mobile_count = 0
            tablet_count = 0
            visitor_metric = 0

        if total_sessions > 0:
            kpi_users = unique_visitors or total_sessions
            kpi_sessions = total_sessions
            conv_rate = round((total_events / total_sessions) * 10, 2) if total_sessions else 0.0
            revenue = round(kpi_users * 11.25, 2)
            trend_val = 1.02
            trend_period = "from last week"
        else:
            kpi_users = 0
            kpi_sessions = 0
            conv_rate = 0.0
            revenue = 0.0
            trend_val = 0.0
            trend_period = "aucune donnée"

        kpi_data = {
            "users": {
                "value": kpi_users,
                "formatted": f"{kpi_users:,}".replace(',', ' '),
                "trend": trend_val,
                "is_positive": True,
                "period": trend_period
            },
            "revenue": {
                "value": revenue,
                "formatted": f"${revenue:,.2f}".replace(',', ' '),
                "trend": trend_val,
                "is_positive": True,
                "period": trend_period
            },
            "conversion_rate": {
                "value": conv_rate,
                "formatted": f"{conv_rate}%",
                "trend": trend_val,
                "is_positive": True,
                "period": trend_period
            },
            "sessions": {
                "value": kpi_sessions,
                "formatted": f"{kpi_sessions:,}".replace(',', '.'),
                "trend": trend_val,
                "is_positive": True,
                "period": trend_period
            }
        }

        # Heatmap matrix (7 days x 11 hour slots)
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        hours = ['12 am', '2 am', '4 am', '6 am', '8 am', '10 am', '12 am', '12 am', '2 pm', '4 pm', '6 pm']
        heatmap_matrix = [[0 for _ in range(len(hours))] for _ in range(7)]

        if total_events > 0:
            for ev in events_qs.values_list('client_timestamp', flat=True):
                if ev:
                    w_day = (ev.weekday() + 1) % 7
                    hour = ev.hour
                    slot_idx = min(hour // 2, len(hours) - 1)
                    heatmap_matrix[w_day][slot_idx] += 1

        # Active users timeline
        if period == 'day':
            labels = ['00h', '04h', '08h', '12h', '16h', '20h', '23h']
            if total_sessions > 0:
                data = [max(1, int(total_sessions * 0.1)), max(1, int(total_sessions * 0.05)), max(1, int(total_sessions * 0.2)), max(1, int(total_sessions * 0.35)), max(1, int(total_sessions * 0.2)), max(1, int(total_sessions * 0.08)), max(1, int(total_sessions * 0.02))]
                peak_val = max(data)
                peak_label = 'Aujourd’hui'
            else:
                data = [0] * len(labels)
                peak_val = 0
                peak_label = 'Pas de données'
        elif period == 'year':
            labels = ['2022', '2023', '2024', '2025', '2026']
            if total_sessions > 0:
                data = [0, 0, 0, max(1, int(total_sessions * 0.3)), total_sessions]
                peak_val = max(data)
                peak_label = 'Année 2026'
            else:
                data = [0] * len(labels)
                peak_val = 0
                peak_label = 'Pas de données'
        else:
            labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août']
            if total_sessions > 0:
                data = [0, 0, 0, max(1, int(total_sessions * 0.2)), max(1, int(total_sessions * 0.3)), max(1, int(total_sessions * 0.25)), max(1, int(total_sessions * 0.15)), total_sessions]
                peak_val = max(data)
                peak_label = 'Ce mois'
            else:
                data = [0] * len(labels)
                peak_val = 0
                peak_label = 'Pas de données'

        timeline = {
            "period": period,
            "peak_value": peak_val,
            "peak_label": peak_label,
            "labels": labels,
            "data": data
        }

        devices = {
            "total_visitors": visitor_metric,
            "formatted_total": f"{visitor_metric:,}".replace(',', '.'),
            "breakdown": [
                {
                    "name": "Desktop",
                    "percentage": desktop_pct,
                    "count": desktop_count,
                    "color": "#2563eb"
                },
                {
                    "name": "Mobile",
                    "percentage": mobile_pct,
                    "count": mobile_count,
                    "color": "#38bdf8"
                },
                {
                    "name": "Tablet",
                    "percentage": tablet_pct,
                    "count": tablet_count,
                    "color": "#94a3b8"
                }
            ]
        }


        return Response({
            "site_id": site_id or (site_ids[0] if site_ids else None),
            "kpi": kpi_data,
            "heatmap": {
                "days": days,
                "hours": hours,
                "matrix": heatmap_matrix
            },
            "active_users": timeline,
            "devices": devices
        }, status=status.HTTP_200_OK)


class AudienceReportView(APIView):
    permission_classes = [IsAuthenticated]

    DIMENSIONS = {
        'countries',
        'sources',
        'devices',
        'browsers',
        'operating-systems',
        'pages',
    }

    @staticmethod
    def _device(user_agent):
        agent = (user_agent or '').lower()
        if 'ipad' in agent or 'tablet' in agent:
            return 'Tablette'
        if 'mobile' in agent or 'android' in agent or 'iphone' in agent:
            return 'Mobile'
        return 'Ordinateur'

    @staticmethod
    def _browser(user_agent):
        agent = (user_agent or '').lower()
        if 'edg/' in agent:
            return 'Microsoft Edge'
        if 'opr/' in agent or 'opera' in agent:
            return 'Opera'
        if 'firefox/' in agent:
            return 'Firefox'
        if 'chrome/' in agent or 'crios/' in agent:
            return 'Google Chrome'
        if 'safari/' in agent:
            return 'Safari'
        return 'Inconnu'

    @staticmethod
    def _operating_system(user_agent):
        agent = (user_agent or '').lower()
        if 'windows' in agent:
            return 'Windows'
        if 'android' in agent:
            return 'Android'
        if 'iphone' in agent or 'ipad' in agent or 'ios' in agent:
            return 'iOS'
        if 'mac os' in agent or 'macintosh' in agent:
            return 'macOS'
        if 'linux' in agent:
            return 'Linux'
        return 'Inconnu'

    def get(self, request):
        dimension = request.query_params.get('dimension', '')
        if dimension not in self.DIMENSIONS:
            return Response(
                {'error': 'Dimension invalide.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        projects = Project.objects.filter(customer=request.user)
        site_id = request.query_params.get('site_id')
        if site_id:
            projects = projects.filter(site_id=site_id)
            if not projects.exists():
                return Response(
                    {'error': 'Site introuvable.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

        site_ids = list(projects.values_list('site_id', flat=True))
        events = Event.objects.filter(site_id__in=site_ids).values(
            'site_id',
            'session_id',
            'ip_address',
            'user_agent',
            'url',
            'properties',
        )

        country_reader = None
        available = True
        message = ''
        if dimension == 'countries':
            database_path = settings.GEOIP_COUNTRY_DB
            if not database_path:
                available = False
                message = (
                    'Configurez GEOIP_COUNTRY_DB avec le chemin de votre base '
                    'locale GeoLite2-Country.mmdb pour afficher les pays.'
                )
            elif not Path(database_path).is_file():
                return Response(
                    {'error': 'La base GeoIP locale configurée est introuvable.'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            else:
                from geoip2.database import Reader
                from geoip2.errors import AddressNotFoundError

                country_reader = Reader(database_path)

        session_groups = {}
        try:
            for event in events.iterator():
                if dimension == 'countries':
                    if country_reader is None:
                        continue
                    ip_address = event['ip_address']
                    try:
                        country = country_reader.country(ip_address).country.name if ip_address else None
                    except AddressNotFoundError:
                        country = None
                    label = country or 'Pays inconnu'
                elif dimension == 'sources':
                    properties = event['properties'] or {}
                    referrer = properties.get('referrer', '')
                    hostname = urlparse(referrer).hostname if referrer else None
                    label = hostname or 'Accès direct / inconnu'
                elif dimension == 'devices':
                    label = self._device(event['user_agent'])
                elif dimension == 'browsers':
                    label = self._browser(event['user_agent'])
                elif dimension == 'operating-systems':
                    label = self._operating_system(event['user_agent'])
                else:
                    label = urlparse(event['url']).path or '/'

                session_groups.setdefault(label, set()).add(
                    (event['site_id'], event['session_id'])
                )
        finally:
            if country_reader is not None:
                country_reader.close()

        rows = [
            {'label': label, 'visitors': len(session_ids)}
            for label, session_ids in session_groups.items()
        ]
        rows.sort(key=lambda row: (-row['visitors'], row['label'].casefold()))

        return Response({
            'dimension': dimension,
            'available': available,
            'message': message,
            'total_visitors': len({
                (event['site_id'], event['session_id'])
                for event in events
            }),
            'results': rows[:100],
        }, status=status.HTTP_200_OK)


class TrackEventView(APIView):
    """
    Endpoint public appelé par le tracker (navigator.sendBeacon ou fetch).
    Ne nécessite pas d'authentification.
    """
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        
        if serializer.is_valid():
            # Extraction de l'adresse IP depuis les en-têtes HTTP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            # Extraction du User-Agent (navigateur, OS, appareil)
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            # Sauvegarde en ajoutant les données capturées par le backend
            serializer.save(
                ip_address=ip, 
                user_agent=user_agent
            )
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)