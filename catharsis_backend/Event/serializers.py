from rest_framework import serializers
from .models import Project, Session, Event, ConversionGoal


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


class ConversionGoalSerializer(serializers.ModelSerializer):
    site_id = serializers.CharField(write_only=True, required=False, allow_blank=True)
    project_site_id = serializers.CharField(source='project.site_id', read_only=True)

    class Meta:
        model = ConversionGoal
        fields = [
            'id',
            'site_id',
            'project_site_id',
            'name',
            'goal_type',
            'target_value',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'project_site_id', 'created_at', 'updated_at']

    def validate_name(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Le nom de l'objectif est requis.")
        return cleaned

    def validate_target_value(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("La cible de conversion est requise.")
        return cleaned

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        raw_site_id = (attrs.pop('site_id', None) or '').strip()

        user_projects = Project.objects.filter(customer=user)
        if raw_site_id:
            project = user_projects.filter(site_id=raw_site_id).first()
            if project is None:
                raise serializers.ValidationError({'site_id': 'Site introuvable pour cet utilisateur.'})
        else:
            project = user_projects.first()
            if project is None:
                raise serializers.ValidationError({'site_id': 'Veuillez d’abord enregistrer un site.'})

        goal_type = attrs.get('goal_type')
        target_value = attrs.get('target_value', '').strip()
        if goal_type == ConversionGoal.GOAL_TYPE_PAGEVIEW_URL and not target_value.startswith('/') and not target_value.startswith('http'):
            target_value = f'/{target_value}'
            attrs['target_value'] = target_value

        if ConversionGoal.objects.filter(
            project=project,
            goal_type=goal_type,
            target_value=target_value,
        ).exists():
            raise serializers.ValidationError({
                'target_value': 'Un objectif de conversion identique existe déjà pour ce site.'
            })

        attrs['project'] = project
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['site_id'] = data.pop('project_site_id', instance.project.site_id)
        return data
