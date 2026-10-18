from django.urls import path
from .views import AudienceReportView, ManageProjectView, AnalyticsDashboardView, TrackEventView

urlpatterns = [
    path('', ManageProjectView.as_view(), name='manage-projects'),
    path('analytics/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    path('audience/', AudienceReportView.as_view(), name='audience-report'),
    path('track-event/', TrackEventView.as_view(), name='track-event'),
]
