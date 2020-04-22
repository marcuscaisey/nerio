from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Url(models.Model):
    name = models.CharField(unique=True, max_length=120)
    target = models.TextField()
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="urls",
        related_query_name="url",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    visits = models.PositiveIntegerField(default=0)
