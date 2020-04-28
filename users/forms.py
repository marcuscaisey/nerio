from django.contrib.auth import forms as auth_forms


class AuthenticationForm(auth_forms.AuthenticationForm):
    error_messages = {
        "invalid_login": (
            "The %(username)s and password provided do not match any of our records."
        ),
        "inactive": "This account is inactive.",
    }
