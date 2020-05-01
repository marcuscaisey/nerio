from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import AuthenticationForm, UserCreationForm


class LoginView(auth_views.LoginView):
    authentication_form = AuthenticationForm
    template_name = "users/login.html"
    redirect_authenticated_user = True


class PasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "users/password_change.html"
    success_url = reverse_lazy("core:home")
    success_message = "Your password has been changed."


class SignupView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")
    success_message = "Your account has been created."
