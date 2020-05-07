from django import forms
from django.forms import TextInput

from .models import URL


class URLCreationForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ("target", "name")
        labels = {
            "target": "URL",
        }
        error_messages = {
            "name": {
                "unique": "This name has already been taken.",
                "max_length": (
                    "Names must be no longer than %(limit_value)s characters."
                ),
            },
        }
        help_texts = {"name": "This will be randomly generated, if left empty."}
        widgets = {
            "target": TextInput,
        }

    def save(self, *args, user=None, **kwargs):
        """Associate the URL with a user on save."""
        url = super().save(commit=False)
        if user is not None and user.is_authenticated:
            url.created_by = user
        url.save()
