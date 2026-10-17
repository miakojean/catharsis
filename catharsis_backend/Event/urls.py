from django.urls import path
from .views import ManageProjectView, AnalyticsDashboardView

urlpatterns = [
    path('', ManageProjectView.as_view(), name='manage-projects'),
    path('analytics/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
]

