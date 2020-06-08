from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from core.models import URL
from helpers.forms import ModelFormIntegrityMixin
from users.forms import AuthenticationForm, UserCreationForm


class EmailChangeView(SuccessMessageMixin, ModelFormIntegrityMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ("email",)
    template_name = "users/email_change.html"
    success_url = reverse_lazy("core:home")
    success_message = "Your email has been changed."

    def get_object(self, queryset=None):
        return self.request.user


class LoginView(auth_views.LoginView):
    authentication_form = AuthenticationForm
    template_name = "users/login.html"
    redirect_authenticated_user = True


class PasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "users/password_change.html"
    success_url = reverse_lazy("core:home")
    success_message = "Your password has been changed."


class PasswordResetView(SuccessMessageMixin, auth_views.PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_url = reverse_lazy("core:home")
    success_message = "An email has been sent to you with instructions on how to reset your password."


class PasswordResetConfirmView(SuccessMessageMixin, auth_views.PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:login")
    success_message = "Your password has been reset."


class SignupView(ModelFormIntegrityMixin, SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")
    success_message = "Your account has been created."

    def form_valid(self, form):
        """
        When a user signs up, assign to them all of the URLs which they have
        already created.
        """
        response = super().form_valid(form)

        session_urls = self.request.session.get("urls", [])
        URL.objects.filter(pk__in=session_urls).update(created_by=self.object)

        return response
