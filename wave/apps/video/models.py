import auto_prefetch
from django.db import models

from wave.utils.media import MediaHelper
from wave.utils.models import UIDTimeBasedModel
from wave.utils.validators import FileValidatorHelper


class Video(UIDTimeBasedModel):
    user = auto_prefetch.ForeignKey("users.User", related_name="user_videos", null=True, on_delete=models.CASCADE)
    media_path = models.CharField(max_length=200, null=True)
    was_captioned = models.BooleanField(default=False)
    captions = models.JSONField(default=dict, null=True)
    srt = models.FileField(
        upload_to=MediaHelper.get_document_upload_path,
        validators=[FileValidatorHelper.validate_subtitle_extension, FileValidatorHelper.validate_subtitle_size],
        null=True,
        blank=True,
        max_length=500,
    )
    media = models.FileField(
        upload_to=MediaHelper.get_video_upload_path,
        validators=[FileValidatorHelper.validate_video_extension, FileValidatorHelper.validate_video_size],
        null=True,
        blank=True,
        max_length=500,
    )

    def embed_srt(self, media_path, srt_path, *args, **kwargs):
        media_path, name = MediaHelper.embed_srt_to_video(media_path, srt_path)
        return media_path, name
