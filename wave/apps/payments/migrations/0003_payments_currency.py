# Generated by Django 4.2.3 on 2023-08-11 16:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0002_payments_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="payments",
            name="currency",
            field=models.CharField(
                choices=[("SAR", "SAR"), ("USD", "USD"), ("CAD", "CAD"), ("NGN", "NGN")],
                default="SAR",
                max_length=200,
                null=True,
            ),
        ),
    ]
