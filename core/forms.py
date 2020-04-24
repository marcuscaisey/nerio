from django import forms
from django.forms import TextInput

from .models import Url


class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ("target", "name")
        labels = {
            "target": "Url",
        }
        help_texts = {"name": "This will be randomly generated, if left empty."}
        widgets = {
            "target": TextInput,
        }
