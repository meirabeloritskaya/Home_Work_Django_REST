# Generated by Django 5.1.3 on 2024-12-05 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_options_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="stripe_price_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="stripe_product_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="stripe_session_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]