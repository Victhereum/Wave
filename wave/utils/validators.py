import os

from django.conf import settings
from django.core.exceptions import ValidationError

_VALID_FILE_EXTENSIONS = [
    ".doc",
    ".docx",
    ".jpg",
    ".pdf",
    ".png",
    ".pptx",
    ".xls",
    ".xlsx",
]

_VALID_AUDIO_EXTENSIONS = [
    ".mp3",
    ".aac",
    ".wav",
]

_VALID_VIDEO_EXTENSIONS = [
    "hls",
    ".avi",
    ".flv",
    ".mkv",
    ".mov",
    ".mp4",
    ".webm",
    ".wmv",
]

_VALID_IMAGE_EXTENSIONS = [
    ".jfif",
    ".jpeg",
    ".jpg",
    ".png",
]

_ALL_VALID_EXTENSIONS = (
    _VALID_FILE_EXTENSIONS
    + _VALID_VIDEO_EXTENSIONS
    + _VALID_AUDIO_EXTENSIONS
    + _VALID_IMAGE_EXTENSIONS
)


class FileValidatorHelper:
    """
    Helper class to validate files
    """

    @staticmethod
    def validate_file_extension(obj):
        """
        Checks that we are using a valid file extension
        """

        ext = os.path.splitext(obj.name)[1]

        if not ext.lower() in _VALID_FILE_EXTENSIONS:
            raise ValidationError(
                "Only pdf, doc, docx, xlsx, xls, jpg, pptx "
                + "and png file is supported."
            )

    @staticmethod
    def validate_multiple_filetype_extension(obj):
        """
        Checks that we are using a valid file extension
        """

        ext = os.path.splitext(obj.name)[1]

        if not ext.lower() in _ALL_VALID_EXTENSIONS:
            raise ValidationError(f"Only {_ALL_VALID_EXTENSIONS} files are supported.")

    @staticmethod
    def validate_audio_extension(obj):
        """
        Checks that we are using a valid audio extension
        """

        ext = os.path.splitext(obj.name)[1]

        if not ext.lower() in _VALID_AUDIO_EXTENSIONS:
            raise ValidationError("Only mp3, aac, wav files are supported.")

    @staticmethod
    def validate_audio_size(obj):
        """
        Checks that file size is not too large
        """
        filesize = obj.size

        if filesize > settings.MAX_AUDIO_SIZE:
            mb = (
                settings.MAX_AUDIO_SIZE / 1048576
            )  # Convert the file size from bytes to MB
            raise ValidationError(
                f"The maximum video size that can be uploaded is {mb}MB"
            )

        return obj

    @staticmethod
    def validate_video_extension(obj):
        """
        Checks that we are using a valid video extension
        """

        ext = os.path.splitext(obj.name)[1]

        if not ext.lower() in _VALID_VIDEO_EXTENSIONS:
            raise ValidationError(
                "Only avi, mp4, mov, wmv, flv, mkv " + "and webm file is supported."
            )

    @staticmethod
    def validate_video_size(obj):
        """
        Checks that file size is not too large
        """
        filesize = obj.size

        if filesize > settings.MAX_VIDEO_SIZE:
            mb = (
                settings.MAX_VIDEO_SIZE / 1048576
            )  # Convert the file size from bytes to MB
            raise ValidationError(
                f"The maximum video size that can be uploaded is {mb}MB"
            )

        return obj

    @staticmethod
    def validate_file_size(obj):
        """
        Checks that file size is not too large
        """
        filesize = obj.size

        if filesize > settings.MAX_VIDEO_SIZE:
            mb = (
                settings.MAX_VIDEO_SIZE / 1048576
            )  # Convert the file size from bytes to MB
            raise ValidationError(
                f"The maximum file size that can be uploaded is {mb}MB"
            )

        return obj

    @staticmethod
    def validate_image_size(obj):
        """
        Checks that logo size is not too large
        """
        filesize = obj.size
        if filesize > 2_097_152:
            raise ValidationError("The maximum file size that can be uploaded is 2MB")

        return obj

    @staticmethod
    def validate_image_extension(obj):
        ext = os.path.splitext(obj.name)[1]

        if not ext.lower() in _VALID_IMAGE_EXTENSIONS:
            raise ValidationError("only jpg, jpeg, jfif and png file supported.")
