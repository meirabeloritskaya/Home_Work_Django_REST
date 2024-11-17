from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview_image = models.ImageField(
        upload_to="course_previews/",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Загрузите изображение-превью для курса",
    )
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Введите описание курса",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока",
        help_text="Введите описание урока",
        blank=True,
        null=True,
    )
    preview_image = models.ImageField(
        upload_to="lesson_previews/",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Загрузите изображение-превью для урока",
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Введите ссылку на видеоурок",
        blank=True,
        null=True,
    )

    course = models.ForeignKey(
        "Course",
        related_name="lessons",
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выберите курс, к которому относится этот урок",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
