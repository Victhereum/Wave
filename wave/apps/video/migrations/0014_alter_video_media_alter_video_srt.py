# Generated by Django 4.2.3 on 2023-10-25 09:15

from django.db import migrations, models
import wave.utils.media
import wave.utils.validators


class Migration(migrations.Migration):
    dependencies = [
        ("video", "0013_alter_video_srt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="media",
            field=models.FileField(
                blank=True,
                max_length=255,
                null=True,
                upload_to=wave.utils.media.MediaHelper.get_video_upload_path,
                validators=[
                    wave.utils.validators.FileValidatorHelper.validate_video_extension,
                    wave.utils.validators.FileValidatorHelper.validate_video_size,
                ],
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="srt",
            field=models.FileField(
                blank=True,
                max_length=255,
                null=True,
                upload_to=wave.utils.media.MediaHelper.get_document_upload_path,
                validators=[
                    wave.utils.validators.FileValidatorHelper.validate_subtitle_extension,
                    wave.utils.validators.FileValidatorHelper.validate_subtitle_size,
                ],
            ),
        ),
    ]
