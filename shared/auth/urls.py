from django.urls import path
from .views import LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login/", LoginView.as_view(), name="global-login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="global-refresh"),
]
