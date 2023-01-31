from datetime import datetime

from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from psqlextra.manager import PostgresManager

from users.utils import validate_phone_number


class Gender(models.TextChoices):
    MALE = "Male", "Мужчина"
    FEMALE = "Female", "Женщина"
    OTHER = "Other", "Другой"


class User(TimeStampedModel):
    """Пользователь."""

    first_name = models.CharField(
        verbose_name="Имя",
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
    )
    city = models.CharField(
        verbose_name="Город",
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
    )
    gender = models.CharField(
        verbose_name="Пол",
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
        choices=Gender.choices,
    )
    birthday = models.DateField(
        verbose_name="День рождения",
    )
    email = models.EmailField(
        verbose_name="Email",
        null=True,
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
    )
    mobile_phone = models.CharField(
        verbose_name="Номер телефона",
        unique=True,
        db_index=True,
        max_length=11,
        validators=[validate_phone_number],
    )

    objects = PostgresManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Interests(models.Model):
    """Увлечение пользователя."""

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="interests",
    )
    interest = models.CharField(
        verbose_name="Увлечение",
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
    )

    objects = PostgresManager()

    class Meta:
        verbose_name = "Увлечение пользователя"
        verbose_name_plural = "Увлечения пользователя"


class UserTag(models.Model):
    """Тег пользователя."""

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="user_tags",
    )
    tag = models.CharField(
        verbose_name="Тег",
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
    )

    objects = PostgresManager()

    class Meta:
        verbose_name = "Тег пользователя"
        verbose_name_plural = "Теги пользователя"


class Photo(models.Model):
    """Фото пользователя."""

    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        default=datetime.utcnow,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="photos",
    )
    url = models.CharField(
        verbose_name="URL изображения",
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
    )
    is_main = models.BooleanField(
        verbose_name="Флаг основного фото",
        default=False,
    )

    objects = PostgresManager()

    class Meta:
        verbose_name = "Фото пользователя"
        verbose_name_plural = "Фото пользователя"


class Friendship(models.Model):
    """Друг пользователя."""

    user_1 = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        verbose_name="Первый пользователь",
        related_name="user_1_friends",
        null=True,
    )
    user_2 = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        verbose_name="Второй пользователь",
        related_name="user_2_friends",
        null=True,
    )
    request_date = models.DateField(
        verbose_name="Дата отправки запроса",
        default=datetime.today,
    )
    approve_date = models.DateField(
        verbose_name="Дата принятия запроса",
        null=True,
    )

    objects = PostgresManager()

    class Meta:
        verbose_name = "Друг пользователя"
        verbose_name_plural = "Друзья пользователя"
