from django.urls import path
from .views import ManageProjectView, AnalyticsDashboardView, TrackEventView

urlpatterns = [
    path('', ManageProjectView.as_view(), name='manage-projects'),
    path('analytics/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    path('track-event/', TrackEventView.as_view(), name='track-event'),
]

