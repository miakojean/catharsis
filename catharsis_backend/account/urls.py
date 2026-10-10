from django.urls import path
from .views import CustomerDetailView, CustomerLoginView

urlpatterns = [
    path("customer/", CustomerDetailView.as_view(), name="customer_detail"),
    path("login/", CustomerLoginView.as_view(), name="customer_login"),
]
