import django_filters

from materials.models import Course, Lesson


class CourseFilter(django_filters.FilterSet):
    # Фильтрация по статусу оплаченности курса
    is_paid = django_filters.BooleanFilter(
        field_name="lessons__payment_date",
        lookup_expr="isnull",
        label="Оплачены ли все уроки",
    )

    class Meta:
        model = Course
        fields = ["is_paid"]


class LessonFilter(django_filters.FilterSet):
    # Фильтрация по дате оплаты
    payment_date = django_filters.DateTimeFilter(
        field_name="payment_date", lookup_expr="exact", label="Дата оплаты"
    )

    # Фильтрация по способу оплаты
    payment_method = django_filters.ChoiceFilter(
        choices=[("cash", "Наличные"), ("transfer", "Перевод")]
    )

    # Фильтрация по курсу
    course = django_filters.ModelChoiceFilter(
        queryset=Course.objects.all(), label="Курс"
    )

    class Meta:
        model = Lesson
        fields = ["payment_date", "payment_method", "course"]
