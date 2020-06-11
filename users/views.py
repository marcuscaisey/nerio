from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from core.models import URL
from users.forms import AuthenticationForm, UserCreationForm


class ModelFormIntegrityMixin:
    """
    To be used in conjunction with the ModelFormMixin. Returns the model form
    filled with errors if an IntegrityError is raised whilst saving the
    associated instance. This class must appear before any other class in the
    inheritance chain which defines a form_valid method.

    This is a solution to the following problem which is caused by a race
    condition when saving the form:

    1. We have the following model and model form:

       class Foo(Model):
           bar = IntegerField(unique=True)

       class FooForm(ModelForm):
           class Meta:
               model = Foo
               fields = ("bar",)

    2. A page contains FooForm.

    3. At the same time, two users submit FooForm with bar = 2.

    4. Both requests are handled, forms are validated and saved. Only one saves
       successfully though, the other fails and raises an IntegrityError because
       there already exists a Foo with bar = 2.
    """

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            form = self.get_form()
            return self.form_invalid(form)


class EmailChangeView(ModelFormIntegrityMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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
    email_template_name = "users/password_reset_text_email.html"
    html_email_template_name = "users/password_reset_html_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_url = reverse_lazy("core:home")
    success_message = "An email has been sent to you with a link to reset your password."


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
