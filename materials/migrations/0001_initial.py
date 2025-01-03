# Generated by Django 5.1.3 on 2024-11-17 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Введите название курса",
                        max_length=255,
                        verbose_name="Название курса",
                    ),
                ),
                (
                    "preview_image",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите изображение-превью для курса",
                        null=True,
                        upload_to="course_previews/",
                        verbose_name="Превью курса",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Введите описание курса",
                        verbose_name="Описание курса",
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Введите название урока",
                        max_length=255,
                        verbose_name="Название урока",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Введите описание урока",
                        verbose_name="Описание урока",
                    ),
                ),
                (
                    "preview_image",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите изображение-превью для урока",
                        null=True,
                        upload_to="lesson_previews/",
                        verbose_name="Превью урока",
                    ),
                ),
                (
                    "video_url",
                    models.URLField(
                        help_text="Введите ссылку на видеоурок",
                        verbose_name="Ссылка на видео",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        help_text="Выберите курс, к которому относится этот урок",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="materials.course",
                        verbose_name="Курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
    ]
