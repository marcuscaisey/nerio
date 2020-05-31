from django.core.validators import RegexValidator, ValidationError
from django.apps import apps


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
