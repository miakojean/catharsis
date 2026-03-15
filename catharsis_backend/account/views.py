from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomerSerializer
from .models import Customer
from django.contrib.auth import authenticate


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
            
        # Générer les tokens d'authentification ou gérer la session ici
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
    
        # Définir les cookies HttpOnly pour les tokens

        response = Response(
            {
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token
            },
            status=status.HTTP_200_OK
        )
            
        
        
