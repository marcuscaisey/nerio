import re

import bs4
import requests
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

PROTOCOL_PATTERN = r"(?i)^https?://"


class Url(models.Model):
    name = models.CharField(unique=True, max_length=120)
    target = models.TextField()
    title = models.TextField()
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

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.normalise_target()
            self.set_title()
        super().save(*args, **kwargs)

    def normalise_target(self):
        """
        Prefix the target with http:// if it doesn't stat with http or https.
        """
        if not re.match(PROTOCOL_PATTERN, self.target):
            self.target = "http://" + self.target

    def set_title(self):
        """
        Set the title to contents of the title tag of the page that the target
        points to. If this page doesn't have a title, or it doesn't exist, then
        set the title to the target with the protocol stripped from the front.
        """
        self.title = re.sub(PROTOCOL_PATTERN, "", self.target)

        try:
            r = requests.get(self.target)
        except requests.ConnectionError:
            return

        soup = bs4.BeautifulSoup(r.content, features="html.parser")
        if soup.title:
            self.title = soup.title.string
