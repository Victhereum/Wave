# Generated by Django 4.2.3 on 2023-10-28 10:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_remove_user_collection_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="collection_id",
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
