from django.urls import path, re_path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.home, name="home"),
    path("url/<int:pk>", views.modify, name="modify"),
    re_path(r"^([a-zA-Z0-9_-]+)/$", views.forward, name="forward"),
]
