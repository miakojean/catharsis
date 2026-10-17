from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer


class CustomerLogoutTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create_user(
            email=config('TEST_ANALYTICS_USER_EMAIL'),
            password=config('TEST_ANALYTICS_USER_PASSWORD')
        )

    def test_logout_blacklists_refresh_token(self):
        refresh = RefreshToken.for_user(self.customer)
        refresh_jti = refresh['jti']

        response = self.client.post(
            '/account/logout/',
            {'refresh': str(refresh)},
            format='json',
        )

        self.assertEqual(response.status_code, 205)
        self.assertTrue(BlacklistedToken.objects.filter(token__jti=refresh_jti).exists())

    def test_logout_rejects_missing_refresh_token(self):
        response = self.client.post('/account/logout/', {}, format='json')

        self.assertEqual(response.status_code, 400)


class CustomerInitialsTests(TestCase):
    def test_initials_from_dotted_email(self):
        customer = Customer.objects.create_user(email='jane.doe@example.com', password=config('TEST_ANALYTICS_USER_PASSWORD'))
        self.assertEqual(customer.initials, 'JD')

    def test_initials_from_underscore_email(self):
        customer = Customer.objects.create_user(email='john_smith@example.com', password=config('TEST_ANALYTICS_USER_PASSWORD'))
        self.assertEqual(customer.initials, 'JS')

    def test_initials_from_hyphenated_email(self):
        customer = Customer.objects.create_user(email='jean-luc@example.com', password=config('TEST_ANALYTICS_USER_PASSWORD'))
        self.assertEqual(customer.initials, 'JL')

    def test_initials_from_single_token_email(self):
        customer = Customer.objects.create_user(email='alexandre@example.com', password=config('TEST_ANALYTICS_USER_PASSWORD'))
        self.assertEqual(customer.initials, 'AL')

    def test_initials_from_short_email(self):
        customer = Customer.objects.create_user(email='q@example.com', password=config('TEST_ANALYTICS_USER_PASSWORD'))
        self.assertEqual(customer.initials, 'Q')


class CustomerMeViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create_user(
            email=config('TEST_ANALYTICS_USER_EMAIL'),
            password=config('TEST_ANALYTICS_USER_PASSWORD'),
            phone_number='+33612345678'
        )

    def test_me_unauthenticated_returns_401(self):
        response = self.client.get('/account/me/')
        self.assertEqual(response.status_code, 401)

    def test_me_authenticated_returns_profile_and_initials(self):
        refresh = RefreshToken.for_user(self.customer)
        token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get('/account/me/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['email'], config('TEST_ANALYTICS_USER_EMAIL'))
        self.assertEqual(data['initials'], 'AW')
        self.assertEqual(data['phone_number'], '+33612345678')
        self.assertNotIn('password', data)

    def test_login_returns_initials(self):
        response = self.client.post(
            '/account/login/',
            {'email': config('TEST_ANALYTICS_USER_EMAIL'), 'password': config('TEST_ANALYTICS_USER_PASSWORD')},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('user', data)
        self.assertEqual(data['user']['email'], config('TEST_ANALYTICS_USER_EMAIL'))
        self.assertEqual(data['user']['initials'], 'AW')

