from django import forms
from django.forms import TextInput

from helpers.forms import PlaceholdersMixin

from .models import URL


class URLCreationForm(PlaceholdersMixin, forms.ModelForm):
    class Meta:
        model = URL
        fields = ("target", "name")
        labels = {
            "target": "URL",
        }
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
