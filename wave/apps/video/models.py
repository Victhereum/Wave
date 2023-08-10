from django.db import models

from wave.utils.media import MediaHelper
from wave.utils.models import UIDTimeBasedModel
from wave.utils.validators import FileValidatorHelper


class Video(UIDTimeBasedModel):
    media = models.FileField(
        upload_to=MediaHelper.get_video_upload_path,
        validators=[FileValidatorHelper.validate_video_extension, FileValidatorHelper.validate_video_size],
    )
    translated = models.BooleanField(default=False)
    captions = models.JSONField(default=dict)
