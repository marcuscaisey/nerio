import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def messages_json(context):
    """Return the messages passed to the template as JSON."""
    try:
        messages = context["messages"]
    except KeyError:
        return

    messages_dict = [
        {"message": m.message, "level": m.level, "tags": m.tags, "extra_tags": m.extra_tags, "level_tag": m.level_tag}
        for m in messages
    ]

    messages_json = json.dumps(messages_dict)
    return mark_safe(messages_json)
