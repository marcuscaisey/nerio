from django.contrib.admin import ModelAdmin, TabularInline, register

from core.models import URL

from .models import User


class URLInline(TabularInline):
    model = URL
    fields = (
        "name",
        "target",
        "title",
        "created_at",
        "visits",
        "is_active",
    )
    ordering = ("created_at",)
    readonly_fields = (
        "target",
        "title",
        "created_at",
        "visits",
    )


@register(User)
class UserAdmin(ModelAdmin):
    date_hierarchy = "date_joined"
    fields = (
        "username",
        "email",
        "date_joined",
        "last_login",
        "is_superuser",
        "groups",
        "user_permissions",
        "is_staff",
        "is_active",
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    inlines = (URLInline,)
    list_display = (
        "username",
        "email",
        "date_joined",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "date_joined",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    readonly_fields = (
        "date_joined",
        "last_login",
    )
    search_fields = (
        "username",
        "email",
    )
