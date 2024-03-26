# Generated by Django 4.2.3 on 2024-03-26 03:23

import auto_prefetch
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("payments", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptions",
            name="user",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="subscriptions", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="subscriptionplan",
            name="priviledges",
            field=models.ManyToManyField(related_name="plans", to="payments.subscriptionpriviledge"),
        ),
    ]