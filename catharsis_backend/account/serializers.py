from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    initials = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = ['id', 'email', 'phone_number', 'initials', 'password', 'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'initials', 'is_active', 'is_staff', 'date_joined']

    def validate(self, attrs):
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({"password": "Ce champ est obligatoire lors de l'inscription."})
        return attrs

    def create(self, validated_data):
        # Utiliser la méthode create_user du UserManager pour hasher le mot de passe
        user = Customer.objects.create_user(**validated_data)
        return user