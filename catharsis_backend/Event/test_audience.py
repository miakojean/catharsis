from decouple import config
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch

from account.models import Customer
from .models import Event, Project


class AudienceReportTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create_user(
            email=config('TEST_ANALYTICS_USER_EMAIL'),
            password=config('TEST_ANALYTICS_USER_PASSWORD'),
        )
        self.project = Project.objects.create(customer=self.customer, name='Audience project')
        refresh = RefreshToken.for_user(self.customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_device_report_counts_unique_visitors_and_hides_ip(self):
        shared_fields = {
            'site_id': self.project.site_id,
            'event_type': 'page_view',
            'url': 'https://example.com/home',
            'client_timestamp': timezone.now(),
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile',
            'ip_address': '203.0.113.4',
        }
        Event.objects.create(session_id='visitor-one', **shared_fields)
        Event.objects.create(session_id='visitor-one', **shared_fields)
        Event.objects.create(
            session_id='visitor-two',
            **{
                **shared_fields,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0',
            },
        )

        response = self.client.get(
            f'/event/audience/?dimension=devices&site_id={self.project.site_id}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_visitors'], 2)
        self.assertEqual(response.json()['results'], [
            {'label': 'Mobile', 'visitors': 1},
            {'label': 'Ordinateur', 'visitors': 1},
        ])
        self.assertNotIn('203.0.113.4', response.content.decode())

    def test_source_report_uses_captured_referrer(self):
        Event.objects.create(
            site_id=self.project.site_id,
            session_id='visitor-one',
            event_type='page_view',
            url='https://example.com/home',
            client_timestamp=timezone.now(),
            properties={'referrer': 'https://search.example/results?q=site'},
        )

        response = self.client.get(
            f'/event/audience/?dimension=sources&site_id={self.project.site_id}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'], [
            {'label': 'search.example', 'visitors': 1},
        ])

    def test_country_report_explains_missing_local_database(self):
        response = self.client.get(
            f'/event/audience/?dimension=countries&site_id={self.project.site_id}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['available'])
        self.assertIn('GEOIP_COUNTRY_DB', response.json()['message'])

    @override_settings(GEOIP_COUNTRY_DB='local-country.mmdb')
    @patch('pathlib.Path.is_file', return_value=True)
    @patch('geoip2.database.Reader')
    def test_country_report_uses_local_geoip_database(self, reader_class, _is_file):
        Event.objects.create(
            site_id=self.project.site_id,
            session_id='visitor-one',
            event_type='page_view',
            url='https://example.com/home',
            client_timestamp=timezone.now(),
            ip_address='203.0.113.4',
        )
        reader_class.return_value.country.return_value.country.name = 'France'

        response = self.client.get(
            f'/event/audience/?dimension=countries&site_id={self.project.site_id}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['available'])
        self.assertEqual(response.json()['results'], [
            {'label': 'France', 'visitors': 1},
        ])
        reader_class.return_value.close.assert_called_once()

    def test_report_rejects_unknown_dimension_and_foreign_site(self):
        invalid_response = self.client.get('/event/audience/?dimension=emails')
        self.assertEqual(invalid_response.status_code, 400)

        other_customer = Customer.objects.create_user(
            email='other-audience@example.com',
            password=config('TEST_ANALYTICS_USER_PASSWORD'),
        )
        other_project = Project.objects.create(customer=other_customer, name='Private project')
        foreign_site_response = self.client.get(
            f'/event/audience/?dimension=devices&site_id={other_project.site_id}'
        )
        self.assertEqual(foreign_site_response.status_code, 404)
