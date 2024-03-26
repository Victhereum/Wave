import auto_prefetch
from django.db import models

from wave.utils.models import UIDTimeBasedModel


class Video(UIDTimeBasedModel):
    user = auto_prefetch.ForeignKey("users.User", related_name="videos", null=True, on_delete=models.CASCADE)
    media_path = models.CharField(max_length=200, null=True)
    was_captioned = models.BooleanField(default=False)
    captions = models.JSONField(default=dict, null=True)
    name = models.CharField(max_length=200, null=True)
    media = models.URLField(
        null=True,
        blank=True,
        max_length=500,
    )
