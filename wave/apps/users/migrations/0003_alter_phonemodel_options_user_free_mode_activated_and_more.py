# Generated by Django 4.2.3 on 2023-08-11 21:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_phonemodel_options_alter_phonemodel_managers_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="phonemodel",
            options={"base_manager_name": "prefetch_manager", "ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="user",
            name="free_mode_activated",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="free_mode_activated_at",
            field=models.DateTimeField(null=True),
        ),
    ]