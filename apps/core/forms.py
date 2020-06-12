from django import forms
from django.forms import TextInput

from .models import URL


class PlaceholdersMixin:
    """
    Sets the placeholders on a Form's widgets. Add a "placeholders" dict to the
    Meta options, which maps field names to placeholder texts.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = getattr(self.Meta, "placeholders", {})
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs["placeholder"] = placeholder


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
