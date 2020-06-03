from django import template

register = template.Library()


@register.filter
def tabindex(field, index):
    """Set the tab index on the filtered field."""
    field.field.widget.attrs["tabindex"] = index
    return field
