from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class UsernameCharactersValidator(RegexValidator):
    regex = "^[a-zA-Z0-9_]+$"
    message = "Usernames can only contain letters, numbers, and underscores."


def validate_username_case_insensitive_unique(username):
    """Validate that no user exists with the same username, ignoring case."""
    user_model = get_user_model()

    try:
        user_model.objects.get_by_natural_key(username)
        raise ValidationError(message=None, code="unique")
    except user_model.DoesNotExist:
        pass
