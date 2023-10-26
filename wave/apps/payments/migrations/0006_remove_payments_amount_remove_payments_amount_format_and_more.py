# Generated by Django 4.2.3 on 2023-08-11 19:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0005_remove_payments_source"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payments",
            name="amount",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="amount_format",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="captured",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="captured_at",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="captured_format",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="currency",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="description",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="fee",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="fee_format",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="invoice_id",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="refunded",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="refunded_at",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="refunded_format",
        ),
        migrations.RemoveField(
            model_name="payments",
            name="status",
        ),
    ]