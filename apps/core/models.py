import random
import re

import bs4
import requests
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.utils import timezone

from . import words
from .validators import (
    URLNameCharacterValidator,
    validate_url_name_doesnt_clash,
)

PROTOCOL_PATTERN = r"(?i)^https?://"


class URL(models.Model):
    name = models.CharField(
        max_length=120,
        blank=True,
        validators=[URLNameCharacterValidator(), validate_url_name_doesnt_clash],
        help_text="This will be randomly generated, if left empty.",
        error_messages={
            "unique": "This name has already been taken.",
            "max_length": "Names must be no longer than %(limit_value)s characters.",
        },
    )
    name_lower = models.CharField(unique=True, max_length=120, blank=True)
    target = models.TextField()
    title = models.TextField(blank=True)
    created_by = models.ForeignKey(
        get_user_model(),
        verbose_name="creator",
        on_delete=models.DO_NOTHING,
        related_name="urls",
        related_query_name="url",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField("created date", default=timezone.now)
    is_active = models.BooleanField("active", default=True)
    visits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        while True:
            try:
                super().save(*args, **kwargs)
                return
            except IntegrityError:
                if self._random_name_required:
                    self._set_random_name()
                else:
                    raise

    def clean(self):
        if self.pk is None:
            self._normalise_target()
            self._set_title()

        if self.name:
            self._random_name_required = False
            self.name_lower = self.name.lower()
            if URL.objects.filter(name_lower=self.name_lower).exclude(pk=self.pk).count() > 0:
                raise ValidationError({"name": ValidationError("This name has already been taken.", code="unique")})
        else:
            self._random_name_required = True
            self._set_random_name()

    def _normalise_target(self):
        """
        Prefix the target with http:// if it doesn't stat with http or https.
        """
        if not re.match(PROTOCOL_PATTERN, self.target):
            self.target = "http://" + self.target

    def _set_random_name(self):
        """
        Set the name to a random combination of two adjectives followed by a
        noun.
        """
        self.name = "".join(word.title() for word in [*random.sample(words.ADJECTIVES, 2), random.choice(words.NOUNS)])
        self.name_lower = self.name.lower()

    def _set_title(self):
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
