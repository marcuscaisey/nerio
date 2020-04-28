from django.contrib.auth import backends


class ModelBackend(backends.ModelBackend):
    def user_can_authenticate(self, user):
        """
        Always allow the user to authenticate to hand off all further checks to
        the AuthenticationForm.
        """
        return True
