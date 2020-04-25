from django.urls import path, re_path

from . import views
from .validators import URL_NAME_PATTERN

app_name = "core"
urlpatterns = [
    path("", views.home, name="home"),
    re_path(URL_NAME_PATTERN, views.forward_url, name="forward"),
]
