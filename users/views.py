from django.contrib.auth import views as auth_views

from users.forms import AuthenticationForm


class LoginView(auth_views.LoginView):
    authentication_form = AuthenticationForm
    template_name = "users/login.html"
    extra_context = {"title": "Login"}
