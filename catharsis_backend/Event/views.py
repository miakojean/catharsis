from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConversionGoal, Project
from .serializers import ConversionGoalSerializer, EventSerializer, ProjectSerializer
from .utils import (
    build_audience_report,
    build_conversions_report,
    build_dashboard,
    get_user_projects,
    normalize_period,
    parse_audience_date_range,
    record_event,
)


class ManageProjectView(ListCreateAPIView):
    """Liste et création des projets de l'utilisateur connecté."""
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    pagination_class = None

    def get_queryset(self):
        return Project.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class AnalyticsDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = get_user_projects(request.user, request.query_params.get('site_id'))
        period = normalize_period(request.query_params.get('period'))
        return Response(build_dashboard(projects, period))


class AudienceReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = get_user_projects(request.user, request.query_params.get('site_id'))
        dimension = request.query_params.get('dimension', '')
        start_date, end_date = parse_audience_date_range(
            request.query_params.get('start_date'),
            request.query_params.get('end_date'),
        )
        return Response(build_audience_report(projects, dimension, start_date, end_date))


class ConversionsView(APIView):
    """Rapport et création d'objectifs de conversion personnalisés."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = get_user_projects(request.user, request.query_params.get('site_id'))
        start_date, end_date = parse_audience_date_range(
            request.query_params.get('start_date'),
            request.query_params.get('end_date'),
        )
        return Response(build_conversions_report(projects, start_date, end_date))

    def post(self, request):
        serializer = ConversionGoalSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConversionGoalDetailView(APIView):
    """Suppression d'un objectif de conversion."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, goal_id):
        goal = ConversionGoal.objects.filter(
            id=goal_id,
            project__customer=request.user,
        ).first()
        if goal is None:
            raise NotFound('Objectif de conversion introuvable.')
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrackEventView(APIView):
    """Endpoint public appelé par le tracker (sendBeacon ou fetch)."""
    permission_classes = [AllowAny]
    authentication_classes = []  # public : évite les 403 CSRF liés à SessionAuthentication

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record_event(serializer, request)
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
