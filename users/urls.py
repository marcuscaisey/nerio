from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("email-change/", views.EmailChangeView.as_view(), name="email-change"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password-change/", views.PasswordChangeView.as_view(), name="password-change"),
    path("password-reset", views.PasswordResetView.as_view(), name="password-reset"),
    path("password-reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password-reset-confirm",),
    path("signup/", views.SignupView.as_view(), name="signup"),
]
