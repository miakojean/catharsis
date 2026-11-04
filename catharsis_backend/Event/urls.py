from django.urls import path
from .views import (
    AnalyticsDashboardView,
    AudienceReportView,
    ConversionGoalDetailView,
    ConversionsView,
    ManageProjectView,
    TrackEventView,
)

urlpatterns = [
    path('', ManageProjectView.as_view(), name='manage-projects'),
    path('analytics/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    path('audience/', AudienceReportView.as_view(), name='audience-report'),
    path('conversions/', ConversionsView.as_view(), name='conversions-report'),
    path('conversions/<uuid:goal_id>/', ConversionGoalDetailView.as_view(), name='conversion-goal-detail'),
    path('track-event/', TrackEventView.as_view(), name='track-event'),
]
