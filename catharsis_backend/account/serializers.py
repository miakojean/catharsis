from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'email', 'phone_number', 'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'is_active', 'is_staff', 'date_joined']