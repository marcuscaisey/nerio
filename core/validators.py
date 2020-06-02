from django.apps import apps
from django.core.validators import RegexValidator, ValidationError
from django.urls import resolve, reverse


class URLNameCharacterValidator(RegexValidator):
    """Validate that a the URL name contains only letters, numbers, -, and _."""

    regex = r"^[a-zA-Z0-9_-]+$"
    message = "This can only contain letters, numbers, -, and _."
    code = "invalid_name"


def validate_url_name_unique(name):
    """Validate that a url name is unique, ignoring case."""
    URL = apps.get_model("core.URL")
    if URL.objects.filter(name__iexact=name).exists():
        raise ValidationError("This name has already been taken.", code="unique")


def validate_url_name_doesnt_clash(name):
    """
    Validate that a url name won't cause a clash with an existing url when
    forwarding.
    """
    potential_url = reverse("core:forward", args=(name,))
    resolved_view = resolve(potential_url)
    if resolved_view.view_name != "core:forward":
        raise ValidationError("This name is has already been taken.", code="unique")
