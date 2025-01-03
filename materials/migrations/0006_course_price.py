# Generated by Django 5.1.3 on 2024-12-05 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0005_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="Введите цену курса",
                max_digits=10,
                null=True,
                verbose_name="Цена курса",
            ),
        ),
    ]
