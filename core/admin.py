from django.contrib.admin import ModelAdmin, register
from django.urls import reverse
from django.utils.html import format_html

from .models import URL


def _list_display(short_description=None, admin_order_field=None):
    """
    Set the short_description and admin_order_field attributes on the decorated
    function.
    """

    def decorator(f):
        if short_description:
            f.short_description = short_description
        if admin_order_field:
            f.admin_order_field = admin_order_field
        return f

    return decorator


@_list_display(short_description="creator", admin_order_field="created_by")
def _user_link(obj):
    """Return a link to the user who created a url."""
    user = obj.created_by
    return format_html(
        "<a href='{url}'>{username}</a>",
        url=reverse("admin:users_user_change", kwargs={"object_id": user.pk}),
        username=getattr(user, user.USERNAME_FIELD),
    )


@register(URL)
class URLAdmin(ModelAdmin):
    date_hierarchy = "created_at"
    fields = (
        "name",
        "target",
        "title",
        "created_by",
        "created_at",
        "visits",
        "is_active",
    )
    list_display = (
        "name",
        "target",
        "title",
        _user_link,
        "created_at",
        "visits",
        "is_active",
    )
    list_display_links = None
    list_filter = (
        "created_by",
        "created_at",
        "visits",
        "is_active",
    )
    list_editable = (
        "name",
        "is_active",
    )
    ordering = ("created_at",)
    readonly_fields = (
        "target",
        "title",
        "created_at",
        "visits",
    )
    search_fields = (
        "name",
        "target",
        "title",
    )
