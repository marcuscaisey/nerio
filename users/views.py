from django.contrib.auth import views as auth_views

from users.forms import AuthenticationForm


class LoginView(auth_views.LoginView):
    authentication_form = AuthenticationForm
    template_name = "templates/form.html"
    extra_context = {
        "title": "Login",
        "submit_value": "Log in",
    }
