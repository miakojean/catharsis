from datetime import datetime
from unittest.mock import patch
import uuid

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from decouple import config

from account.models import Customer
from .models import ConversionGoal, Project, Session, Event


class AnalyticsDashboardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create_user(
            email=config('TEST_ANALYTICS_USER_EMAIL'),
            password=config('TEST_ANALYTICS_USER_PASSWORD')
        )
        self.project = Project.objects.create(
            customer=self.customer,
            name='Test Analytics Project'
        )
        refresh = RefreshToken.for_user(self.customer)
        self.token = str(refresh.access_token)

    def test_analytics_unauthenticated_returns_401(self):
        response = self.client.get('/event/analytics/')
        self.assertEqual(response.status_code, 401)

    def test_analytics_authenticated_returns_all_metrics(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/event/analytics/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('kpi', data)
        self.assertIn('users', data['kpi'])
        self.assertIn('revenue', data['kpi'])
        self.assertIn('conversion_rate', data['kpi'])
        self.assertIn('sessions', data['kpi'])

        self.assertIn('heatmap', data)
        self.assertEqual(len(data['heatmap']['days']), 7)
        self.assertEqual(len(data['heatmap']['hours']), 12)
        self.assertEqual(len(data['heatmap']['matrix']), 7)

        self.assertIn('active_users', data)
        self.assertIn('data', data['active_users'])
        self.assertIn('labels', data['active_users'])

        self.assertIn('devices', data)
        self.assertIn('total_visitors', data['devices'])
        self.assertIn('breakdown', data['devices'])
        self.assertEqual(len(data['devices']['breakdown']), 3)

        # Asserts zero everywhere when no visits recorded
        self.assertEqual(data['kpi']['users']['value'], 0)
        self.assertEqual(data['kpi']['sessions']['value'], 0)
        self.assertEqual(data['kpi']['revenue']['value'], 0.0)
        self.assertEqual(data['devices']['total_visitors'], 0)
        self.assertEqual(data['active_users']['peak_value'], 0)


    def test_analytics_with_real_sessions_and_devices(self):
        # Create 2 desktop sessions, 1 mobile session
        s1 = Session.objects.create(
            project=self.project,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'
        )
        s2 = Session.objects.create(
            project=self.project,
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        )
        s3 = Session.objects.create(
            project=self.project,
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) Mobile'
        )

        Event.objects.create(
            site_id=self.project.site_id,
            session_id=str(s1.session_id),
            event_type='click',
            url='https://example.com/checkout',
            client_timestamp=timezone.now()
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(f'/event/analytics/?site_id={self.project.site_id}')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['kpi']['sessions']['value'], 3)
        self.assertEqual(data['devices']['total_visitors'], 3)

        breakdown = {d['name']: d['percentage'] for d in data['devices']['breakdown']}
        self.assertEqual(breakdown['Desktop'], 66.7)
        self.assertEqual(breakdown['Mobile'], 33.3)

    def test_analytics_period_param(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        for period in ['day', 'month', 'year']:
            response = self.client.get(f'/event/analytics/?period={period}')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['active_users']['period'], period)
            self.assertTrue(len(data['active_users']['labels']) > 0)

    @patch('Event.utils.timezone.localtime')
    def test_dashboard_uses_database_sessions_for_timeline_and_period_trends(self, localtime):
        now = timezone.make_aware(datetime(2024, 6, 15, 12))
        localtime.return_value = now

        session_times = [
            datetime(2024, 6, 15, 1),
            datetime(2024, 6, 15, 3),
            datetime(2024, 6, 15, 5),
            datetime(2024, 6, 3, 10),
            datetime(2024, 2, 4, 10),
            datetime(2024, 6, 14, 11),
        ]
        for timestamp in session_times:
            session = Session.objects.create(project=self.project)
            Session.objects.filter(pk=session.pk).update(
                started_at=timezone.make_aware(timestamp),
            )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        day_response = self.client.get(
            f'/event/analytics/?site_id={self.project.site_id}&period=day'
        )
        self.assertEqual(day_response.status_code, 200)
        day_data = day_response.json()
        self.assertEqual(day_data['active_users']['labels'], [
            '00h', '04h', '08h', '12h', '16h', '20h',
        ])
        self.assertEqual(day_data['active_users']['data'], [2, 1, 0, 0, 0, 0])
        self.assertEqual(day_data['kpi']['sessions']['value'], 3)
        self.assertEqual(day_data['kpi']['sessions']['trend'], 200.0)
        self.assertEqual(day_data['kpi']['sessions']['period'], 'vs période précédente')
        self.assertEqual(day_data['kpi']['revenue']['formatted'], '—')
        self.assertEqual(day_data['kpi']['revenue']['period'], 'Non suivi')
        self.assertEqual(day_data['kpi']['conversion_rate']['formatted'], '—')
        self.assertEqual(day_data['kpi']['conversion_rate']['period'], 'Non suivi')

        month_data = self.client.get(
            f'/event/analytics/?site_id={self.project.site_id}&period=month'
        ).json()['active_users']
        self.assertEqual(len(month_data['labels']), 30)
        self.assertEqual(month_data['data'][2], 1)
        self.assertEqual(month_data['data'][14], 3)

        year_data = self.client.get(
            f'/event/analytics/?site_id={self.project.site_id}&period=year'
        ).json()['active_users']
        self.assertEqual(len(year_data['labels']), 12)
        self.assertEqual(year_data['data'][1], 1)
        self.assertEqual(year_data['data'][5], 5)


class ConversionGoalsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create_user(
            email=config('TEST_ANALYTICS_USER_EMAIL'),
            password=config('TEST_ANALYTICS_USER_PASSWORD')
        )
        self.project = Project.objects.create(
            customer=self.customer,
            name='Conversion Test Project'
        )
        refresh = RefreshToken.for_user(self.customer)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_list_and_delete_conversion_goals(self):
        # 1. Create custom_event goal
        res1 = self.client.post('/event/conversions/', {
            'site_id': self.project.site_id,
            'name': 'Inscription Newsletter',
            'goal_type': 'custom_event',
            'target_value': 'form_submit',
        }, format='json')
        self.assertEqual(res1.status_code, 201)
        goal1_id = res1.json()['id']

        # 2. Create pageview_url goal
        res2 = self.client.post('/event/conversions/', {
            'site_id': self.project.site_id,
            'name': 'Visite Page Tarifs',
            'goal_type': 'pageview_url',
            'target_value': '/pricing',
        }, format='json')
        self.assertEqual(res2.status_code, 201)

        # 3. Simulate 4 sessions: 1 triggers form_submit, 2 visit /pricing
        now = timezone.now()
        sessions = [Session.objects.create(project=self.project) for _ in range(4)]

        # Session 0: form_submit + /pricing (both goals)
        Event.objects.create(
            site_id=self.project.site_id,
            session_id=str(sessions[0].session_id),
            event_type='form_submit',
            url='https://example.com/signup',
            client_timestamp=now,
        )
        Event.objects.create(
            site_id=self.project.site_id,
            session_id=str(sessions[0].session_id),
            event_type='page_view',
            url='https://example.com/pricing',
            client_timestamp=now,
        )
        # Session 1: /pricing only
        Event.objects.create(
            site_id=self.project.site_id,
            session_id=str(sessions[1].session_id),
            event_type='page_view',
            url='https://example.com/pricing',
            client_timestamp=now,
        )
        # Sessions 2 & 3: non-converting page_view
        for s in sessions[2:]:
            Event.objects.create(
                site_id=self.project.site_id,
                session_id=str(s.session_id),
                event_type='page_view',
                url='https://example.com/',
                client_timestamp=now,
            )

        # 4. Get conversions report
        report_res = self.client.get(f'/event/conversions/?site_id={self.project.site_id}')
        self.assertEqual(report_res.status_code, 200)
        report = report_res.json()
        self.assertEqual(report['total_sessions'], 4)
        self.assertEqual(report['total_conversions'], 3)
        self.assertEqual(report['converted_sessions'], 2)
        self.assertEqual(report['conversion_rate'], 50.0)

        goals_by_name = {g['name']: g for g in report['goals']}
        self.assertEqual(goals_by_name['Inscription Newsletter']['conversions_count'], 1)
        self.assertEqual(goals_by_name['Inscription Newsletter']['conversion_rate'], 25.0)
        self.assertEqual(goals_by_name['Visite Page Tarifs']['conversions_count'], 2)
        self.assertEqual(goals_by_name['Visite Page Tarifs']['conversion_rate'], 50.0)

        # 5. Check dashboard KPI reflects dynamic conversion_rate
        dash_res = self.client.get(f'/event/analytics/?site_id={self.project.site_id}')
        self.assertEqual(dash_res.status_code, 200)
        self.assertEqual(dash_res.json()['kpi']['conversion_rate']['value'], 50.0)
        self.assertEqual(dash_res.json()['kpi']['conversion_rate']['formatted'], '50.0%')

        # 6. Delete goal 1
        del_res = self.client.delete(f'/event/conversions/{goal1_id}/')
        self.assertEqual(del_res.status_code, 204)
        self.assertEqual(ConversionGoal.objects.filter(project=self.project).count(), 1)
