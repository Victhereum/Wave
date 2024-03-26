# Generated by Django 4.2.3 on 2024-03-24 16:26

import auto_prefetch
from django.conf import settings
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("video", "0019_rename_bunny_id_video_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="user",
            field=auto_prefetch.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="videos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
