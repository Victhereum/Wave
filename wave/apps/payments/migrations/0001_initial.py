# Generated by Django 4.2.3 on 2023-08-11 15:53

import auto_prefetch
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Payments",
            fields=[
                ("visible", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.CharField(editable=False, max_length=120, primary_key=True, serialize=False, unique=True),
                ),
                ("amount", models.PositiveIntegerField(null=True)),
                ("amount_format", models.CharField(max_length=50)),
                ("status", models.CharField(max_length=10, null=True)),
                ("invoice_id", models.CharField(null=True, verbose_name=120)),
                ("refunded", models.BooleanField(default=False)),
                ("refunded_at", models.DateTimeField(null=True)),
                ("refunded_format", models.CharField(max_length=50)),
                ("captured", models.BooleanField(default=False)),
                ("captured_at", models.DateTimeField(null=True)),
                ("captured_format", models.CharField(max_length=50)),
                ("fee", models.PositiveIntegerField(null=True)),
                ("fee_format", models.CharField(max_length=50, null=True)),
                ("source", models.JSONField(default=dict)),
                (
                    "user",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_payments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
