from celery import shared_task
from django.core.mail import send_mail
from materials.models import Subscription
from django.conf import settings


@shared_task
def send_course_update_email(course_id):
    # Получаем курс по ID
    subscriptions = Subscription.objects.filter(course_id=course_id)

    # Получаем всех пользователей, подписанных на курс
    for subscription in subscriptions:
        user_email = subscription.user.email
        course = subscription.course

        # Отправляем письмо пользователю
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message=f"Здравствуйте! Курс {course.title} был обновлен. Загляните, чтобы узнать больше!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
        )
