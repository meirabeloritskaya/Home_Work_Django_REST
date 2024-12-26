from urllib.parse import urlparse

from django.core.exceptions import ValidationError


class VideoURLValidator:
    """
    Валидатор для проверки ссылок на видео. Допускаются только ссылки на youtube.com.
    """

    def __call__(self, value):
        print(f"Value received: {value}")

        if value is None or value == "":
            return

        if not isinstance(value, str):
            raise ValidationError("Значение должно быть строкой.")

        parsed_url = urlparse(value)
        print(f"Parsed URL: {parsed_url}")
        if parsed_url.netloc not in ["www.youtube.com", "youtube.com"]:
            raise ValidationError("Допустимы только ссылки на youtube.com")
