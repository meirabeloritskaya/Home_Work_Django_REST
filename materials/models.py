from django.db import models

from django.conf import settings


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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courses', on_delete=models.CASCADE, null=True,)

    def is_paid(self):
        # Проверяем, оплачены ли все уроки
        return all(lesson.payment_date is not None for lesson in self.lessons.all())

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

    payment_date = models.DateTimeField(
        verbose_name="Дата оплаты",
        help_text="Дата, когда был произведен платеж",
        null=True,
        blank=True,
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[("cash", "Наличные"), ("transfer", "Перевод")],
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
        null=True,
        blank=True,
    )

    course = models.ForeignKey(
        "Course",
        related_name="lessons",
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выберите курс, к которому относится этот урок",
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lessons', on_delete=models.CASCADE, null=True,)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
