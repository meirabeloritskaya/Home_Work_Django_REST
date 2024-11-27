from django.core.exceptions import ValidationError
from urllib.parse import urlparse


class VideoURLValidator:
    """
    Валидатор для проверки ссылок на видео. Допускаются только ссылки на youtube.com.
    """

    def __call__(self, value):
        parsed_url = urlparse(value)
        if parsed_url.netloc not in ["www.youtube.com", "youtube.com"]:
            raise ValidationError("Допустимы только ссылки на youtube.com")
