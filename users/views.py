from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .models import Payment
from .serializers import PaymentSerializer
from materials.models import Course, Lesson
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.generics import CreateAPIView

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .services.stripe_service import (
    create_product,
    create_price,
    create_checkout_session,
)


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentFilter(filters.FilterSet):
    course = filters.ModelChoiceFilter(queryset=Course.objects.all())
    lesson = filters.ModelChoiceFilter(queryset=Lesson.objects.all())
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)
    payment_date = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_method", "payment_date"]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]  # по умолчанию сортировка по дате оплаты


class CreatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        # Создаем продукт и цену в Stripe
        product = create_product(course.title, course.description)
        price = create_price(product["id"], course.price)

        # Создаем сессию для оплаты
        success_url = "http://127.0.0.1:8000/payment/success/"
        cancel_url = "http://127.0.0.1:8000/payment/cancel/"
        session = create_checkout_session(price["id"], success_url, cancel_url)

        # Сохраняем данные в БД
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            stripe_product_id=product["id"],
            stripe_price_id=price["id"],
            stripe_session_id=session["id"],
        )

        return Response({"payment_url": session["url"], "payment_id": payment.id}, status=status.HTTP_201_CREATED)
