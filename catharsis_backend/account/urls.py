from django.urls import path
from .views import CustomerDetailView, CustomerLoginView, CustomerLogoutView, CustomerMeView

urlpatterns = [
    path("customer/", CustomerDetailView.as_view(), name="customer_detail"),
    path("login/", CustomerLoginView.as_view(), name="customer_login"),
    path("logout/", CustomerLogoutView.as_view(), name="customer_logout"),
    path("me/", CustomerMeView.as_view(), name="customer_me"),
]

