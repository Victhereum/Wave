# Generated by Django 4.2.3 on 2023-12-13 20:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("video", "0017_remove_video_collection_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="bunny_id",
            field=models.CharField(max_length=200, null=True),
        ),
    ]