from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from .serializers import CustomerSerializer
from .models import Customer
from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


def _set_auth_cookies(response, access_token, refresh_token):
    response.set_cookie(
        settings.REST_AUTH['JWT_AUTH_COOKIE'],
        access_token,
        max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
        httponly=True,
        secure=settings.REST_AUTH['JWT_AUTH_SECURE'],
        samesite=settings.REST_AUTH['JWT_AUTH_SAMESITE'],
        path='/',
    )
    response.set_cookie(
        settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE'],
        refresh_token,
        max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
        httponly=True,
        secure=settings.REST_AUTH['JWT_AUTH_SECURE'],
        samesite=settings.REST_AUTH['JWT_AUTH_SAMESITE'],
        path='/',
    )
    return response


def _clear_auth_cookies(response):
    for cookie_name in (
        settings.REST_AUTH['JWT_AUTH_COOKIE'],
        settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE'],
    ):
        response.delete_cookie(
            cookie_name,
            path='/',
            samesite=settings.REST_AUTH['JWT_AUTH_SAMESITE'],
        )
    return response


class CustomerCsrfView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'csrfToken': get_token(request)})


class CustomerDetailView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer =  CustomerSerializer(data=request.data)

        try:
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {
                        "message": "Customer created successfully",
                        "customer": CustomerSerializer(user).data
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CustomerLoginView(APIView):

    permission_classes = [AllowAny]

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validation de base pour s'assurer que les champs sont présents
        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Tentative de récupération de l'utilisateur par email
        if email:
            try:
                user = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response(
                    {"error": "Invalid email or password."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        user = authenticate(request, email=email, password=password)

        # Verification du statut actif de l'utilisateur
        if user is not None:
            if not user.is_active:
                return Response(
                    {"error": "Account is inactive."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # Générer les tokens d'authentification ou gérer la session ici
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
    
        response = Response(
            {
                "message": "Login successful",
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "initials": user.initials
                }
            },
            status=status.HTTP_200_OK
        )
        return _set_auth_cookies(response, access_token, refresh_token)


class CustomerMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomerSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerLogoutView(APIView):

    permission_classes = [AllowAny]

    @method_decorator(csrf_protect)
    def post(self, request):
        refresh_token = request.COOKIES.get(settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE'])
        if not refresh_token:
            return _clear_auth_cookies(Response(status=status.HTTP_205_RESET_CONTENT))

        serializer = TokenBlacklistSerializer(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)
        return _clear_auth_cookies(Response(status=status.HTTP_205_RESET_CONTENT))
