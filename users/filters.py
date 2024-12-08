# from rest_framework import permissions
from django_filters import rest_framework as filters

from materials.models import Course, Lesson

from .models import Payment


class PaymentFilter(filters.FilterSet):
    course = filters.ModelChoiceFilter(queryset=Course.objects.all())
    lesson = filters.ModelChoiceFilter(queryset=Lesson.objects.all())
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)
    payment_date = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_method", "payment_date"]
