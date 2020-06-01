from django import forms
from django.forms import TextInput

from helpers.forms import PlaceholdersMixin

from .models import URL

_url_name_error_messages = {
    "unique": "This name has already been taken.",
    "max_length": "Names must be no longer than %(limit_value)s characters.",
}


class URLCreationForm(PlaceholdersMixin, forms.ModelForm):
    class Meta:
        model = URL
        fields = ("target", "name")
        labels = {
            "target": "URL",
        }
        error_messages = {
            "name": _url_name_error_messages,
        }
        help_texts = {"name": "This will be randomly generated, if left empty."}
        widgets = {
            "target": TextInput,
        }
        placeholders = {
            "target": "https://www.reddit.com/r/django",
            "name": "django-sub",
        }


class URLRenamingForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ("name",)
        error_messages = {
            "name": _url_name_error_messages,
        }
