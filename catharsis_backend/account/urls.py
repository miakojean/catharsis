from django.urls import path
from .views import CustomerCsrfView, CustomerDetailView, CustomerLoginView, CustomerLogoutView, CustomerMeView

urlpatterns = [
    path("csrf/", CustomerCsrfView.as_view(), name="csrf"),
    path("customer/", CustomerDetailView.as_view(), name="customer_detail"),
    path("login/", CustomerLoginView.as_view(), name="customer_login"),
    path("logout/", CustomerLogoutView.as_view(), name="customer_logout"),
    path("me/", CustomerMeView.as_view(), name="customer_me"),
]
