from rest_framework import serializers
from .models import Project, Session, Event

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            'id',
            'site_id',
            'name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'creatd_at'
        ]

class SessionSerializer(serializers.ModelSerializer):

    project = ProjectSerializer()

    class Meta:
        model = Session
        fields = [
            'id',
            'project',
            'session_id',
            'ip_address',
            'user_agent',
            'created_at',
            'updated_at',
        ]
