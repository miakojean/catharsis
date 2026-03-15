from django.urls import path
from .views import (CustomerDetailView)

urlpatterns = [
    path("customer/", CustomerDetailView.as_view(), name="customer_detail"),
]
