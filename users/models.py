from django.contrib.auth import models as auth_models
from django.db import models


class UserManager(auth_models.UserManager):
    def get_by_natural_key(self, username):
        """Ignore case when querying by username."""
        return self.get(**{f"{self.model.USERNAME_FIELD}__iexact": username})

    @classmethod
    def normalize_email(cls, email):
        """Normalize the email address by lowercasing it."""
        return email.lower()


class User(auth_models.AbstractUser):
    email = models.EmailField(
        "email address", unique=True, error_messages={"unique": "A user with that email already exists."}
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
