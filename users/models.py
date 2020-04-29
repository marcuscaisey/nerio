from django.contrib.auth import models as auth_models


class UserManager(auth_models.UserManager):
    def get_by_natural_key(self, username):
        """Ignore case when querying by username."""
        return self.get(**{f"{self.model.USERNAME_FIELD}__iexact": username})


class User(auth_models.AbstractUser):
    objects = UserManager()
