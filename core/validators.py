from django.core.validators import RegexValidator

URL_NAME_PATTERN = r"^([a-zA-Z0-9_-]+)$"


class URLNameValidator(RegexValidator):
    """Validate that a the url name contains only letters, numbers, -, and _."""

    regex = URL_NAME_PATTERN
    message = "This can only contain letters, numbers, -, and _."
    code = "invalid_name"
