#!/usr/bin/env python3
"""Envoie du trafic simulé à /event/track-event/ pour tester les rapports d'audience.

Exemple :
    python seed_events.py --site-id 2d24034fd9 --sessions 200
"""
import argparse
import json
import random
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone

# (referrer, poids) — None = accès direct
REFERRERS = [
    ('https://www.google.com/search?q=catharsis', 35),
    ('https://www.facebook.com/', 15),
    ('https://www.linkedin.com/feed/', 10),
    ('https://x.com/', 8),
    ('https://news.ycombinator.com/', 5),
    ('https://www.bing.com/search?q=bien-etre', 5),
    (None, 22),
]

# (user-agent, poids)
USER_AGENTS = [
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 30),
    ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1', 20),
    ('Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36', 20),
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15', 8),
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0', 7),
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0', 7),
    ('Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1', 4),
    ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/110.0.0.0', 2),
    ('Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0', 2),
]

# IP publiques (pays approximatifs, selon la base GeoIP utilisée)
IPS = [
    '8.8.8.8',          # États-Unis
    '80.67.169.12',     # France
    '213.186.33.5',     # France
    '202.12.27.33',     # Japon
    '1.1.1.1',          # Australie
]

PAGES = ['/', '/', '/about', '/pricing', '/contact', '/blog']


def weighted(choices):
    return random.choices([c[0] for c in choices], weights=[c[1] for c in choices])[0]


def send(endpoint, payload, user_agent, ip):
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode(),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': user_agent,
            'X-Forwarded-For': ip,
        },
    )
    with urllib.request.urlopen(request, timeout=10):
        pass


def simulate_session(endpoint, site_id, base_url, days):
    session_id = str(uuid.uuid4())
    user_agent, ip = weighted(USER_AGENTS), random.choice(IPS)
    referrer = weighted(REFERRERS)
    moment = datetime.now(timezone.utc) - timedelta(
        days=random.uniform(0, days), seconds=random.randint(0, 86400)
    )

    sent = 0
    for step in range(random.randint(1, 6)):
        moment += timedelta(seconds=random.randint(5, 90))
        page = random.choice(PAGES)
        is_click = step > 0 and random.random() < 0.3
        properties = {'referrer': referrer or ''} if step == 0 else {}
        if is_click:
            properties.update({'tag': 'button', 'className': 'main__button'})
        send(endpoint, {
            'site_id': site_id,
            'session_id': session_id,
            'event_type': 'click' if is_click else 'pageview',
            'url': f'{base_url}{page}',
            'client_timestamp': moment.isoformat().replace('+00:00', 'Z'),
            'properties': properties,
        }, user_agent, ip)
        sent += 1
    return sent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-id', required=True)
    parser.add_argument('--sessions', type=int, default=100)
    parser.add_argument('--days', type=int, default=14, help="étalement des dates (jours)")
    parser.add_argument('--endpoint', default='http://localhost:8000/event/track-event/')
    parser.add_argument('--base-url', default='https://catharsis.test', help="domaine des pages simulées")
    parser.add_argument('--seed', type=int, help="graine aléatoire (résultats reproductibles)")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    events = failures = 0
    for _ in range(args.sessions):
        try:
            events += simulate_session(args.endpoint, args.site_id, args.base_url, args.days)
        except urllib.error.HTTPError as error:
            failures += 1
            if failures <= 3:
                print(f'HTTP {error.code} : {error.read().decode()[:200]}')
        except urllib.error.URLError as error:
            raise SystemExit(f"Impossible de joindre {args.endpoint} : {error.reason}")

    print(f'{args.sessions - failures} sessions envoyées ({events} événements), {failures} échec(s).')


if __name__ == '__main__':
    main()