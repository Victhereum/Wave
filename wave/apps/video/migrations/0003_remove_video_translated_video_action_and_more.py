# Generated by Django 4.2.3 on 2023-08-12 11:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("video", "0002_remove_video_media"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="video",
            name="translated",
        ),
        migrations.AddField(
            model_name="video",
            name="action",
            field=models.CharField(
                choices=[("translate", "translate"), ("transcribe", "transcribe")], default="transcribe"
            ),
        ),
        migrations.AddField(
            model_name="video",
            name="media_path",
            field=models.CharField(max_length=200, null=True),
        ),
    ]