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
        read_only_fields = ['id', 'site_id', 'created_at', 'updated_at']


class SessionSerializer(serializers.ModelSerializer):

    project = ProjectSerializer(read_only=True)

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


class EventSerializer(serializers.ModelSerializer):
    # Le tracker envoie un UUID ; on le valide car il sert aussi à créer la Session.
    session_id = serializers.UUIDField()
    # Garantit un objet JSON (et non une liste ou une chaîne) pour properties.
    properties = serializers.DictField(required=False)

    class Meta:
        model = Event
        fields = [
            'site_id',
            'session_id',
            'event_type',
            'url',
            'client_timestamp',
            'properties',
        ]