# Generated by Django 4.2.3 on 2023-10-28 09:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_user_date_joined"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="collection_created",
            field=models.BooleanField(default=False),
        ),
    ]
