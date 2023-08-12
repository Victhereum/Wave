import auto_prefetch
from django.db import models

from wave.utils.models import UIDTimeBasedModel


class Video(UIDTimeBasedModel):
    user = auto_prefetch.ForeignKey("users.User", related_name="user_videos", null=True, on_delete=models.CASCADE)
    media_path = models.CharField(max_length=200, null=True)
    was_captioned = models.BooleanField(default=False)
    captions = models.JSONField(default=dict)
