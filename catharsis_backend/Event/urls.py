from django.urls import path
from .views import ManageProjectView

urlpatterns = [
    path('', ManageProjectView.as_view(), name='manage-projects')
]
