from django.contrib.auth import models as auth_models
from django.db import models

from .validators import (
    UsernameCharactersValidator,
    validate_username_case_insensitive_unique,
)


class UserManager(auth_models.UserManager):
    def get_by_natural_key(self, username):
        """Ignore case when querying by username."""
        return self.get(**{f"{self.model.USERNAME_FIELD}__iexact": username})


class User(auth_models.AbstractUser):
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text="150 characters or fewer. Letters, digits, and underscores only.",
        validators=[UsernameCharactersValidator(), validate_username_case_insensitive_unique],
        error_messages={"unique": "A user with that username already exists."},
    )

    objects = UserManager()
