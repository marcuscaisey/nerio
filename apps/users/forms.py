from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.urls import reverse


class AuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["invalid_login"] = "The %(username)s and password provided do not match any of our records."
        self.fields["password"].help_text = f"<a href='{reverse('users:password-reset')}'>Forgot password?</a>"


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)
