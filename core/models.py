import random
import re

import bs4
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError, models
from django.urls import reverse
from django.utils import timezone

from . import words
from .validators import URLNameValidator

PROTOCOL_PATTERN = r"(?i)^https?://"


class URL(models.Model):
    name = models.CharField(
        unique=True, max_length=120, blank=True, validators=[URLNameValidator()]
    )
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
        saved = False

        if self.pk is None:
            self.normalise_target()
            self.set_title()

        if not self.name:
            while True:
                try:
                    self.set_random_name()
                    super().save(*args, **kwargs)
                    saved = True
                    break
                except IntegrityError:
                    pass

        if not saved:
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return settings.ROOT_URL + reverse("core:forward", args=(self.name,))

    def normalise_target(self):
        """
        Prefix the target with http:// if it doesn't stat with http or https.
        """
        if not re.match(PROTOCOL_PATTERN, self.target):
            self.target = "http://" + self.target

    def set_random_name(self):
        """
        Set the name to a random combination of two adjectives followed by a
        noun.
        """
        self.name = "".join(
            word.title()
            for word in [
                *random.sample(words.ADJECTIVES, 2),
                random.choice(words.NOUNS),
            ]
        )

    def set_title(self):
        """
        Set the title to contents of the title tag of the page that the target
        points to. If this page doesn't have a title, or the GET request to the
        target doesn't return a 2xx status code, or an exception is raised when
        making the GET request, then set the title to the target with the
        protocol stripped from the front and the path stripped from the back.
        """
        target_without_protocol = re.sub(PROTOCOL_PATTERN, "", self.target)
        self.title = target_without_protocol.split("/")[0]

        try:
            r = requests.get(self.target)
        except Exception:
            return

        if not 200 <= r.status_code < 300:
            return

        soup = bs4.BeautifulSoup(r.content, features="html.parser")
        if soup.title:
            self.title = soup.title.string
