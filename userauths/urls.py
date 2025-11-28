from django.urls import path

from userauths import views
from .api_views import api_register, api_login

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.register_view, name="sign-up"),
    path("sign-in/", views.login_view, name="sign-in"),
    path("sign-out/", views.logout_view, name="sign-out"),


        # API endpoints
    path("api/register/", api_register, name="api_register"),
    path("api/login/", api_login, name="api_login"),
]