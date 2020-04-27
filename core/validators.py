from django.core.validators import RegexValidator


class URLNameValidator(RegexValidator):
    """Validate that a the URL name contains only letters, numbers, -, and _."""

    regex = r"^[a-zA-Z0-9_-]+$"
    message = "This can only contain letters, numbers, -, and _."
    code = "invalid_name"
