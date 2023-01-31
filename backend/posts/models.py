from datetime import datetime

from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from psqlextra.manager import PostgresManager
from psqlextra.models import PostgresPartitionedModel
from psqlextra.types import PostgresPartitioningMethod

from users.models import User


class Post(TimeStampedModel):
    """Пост."""

    title = models.CharField(
        verbose_name="Заголовок",
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
    )
    content = models.TextField(
        verbose_name="Содержимое",
        max_length=1500,
    )
    user = models.ForeignKey(
        to=User,
        verbose_name="Пользователь",
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
    )
    likes = models.PositiveBigIntegerField(
        verbose_name="Кол-во лайков",
        default=0,
    )

    objects = PostgresManager()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class PostTag(models.Model):
    """Тег поста."""

    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        verbose_name="Пост",
        related_name="post_tags",
    )
    tag = models.CharField(
        verbose_name="Тег",
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
    )

    objects = PostgresManager()

    class Meta:
        verbose_name = "Тег поста"
        verbose_name_plural = "Теги поста"


class Comment(PostgresPartitionedModel):
    class PartitioningMeta:
        method = PostgresPartitioningMethod.HASH
        key = ["id"]

    content = models.TextField(
        verbose_name="Контент",
        max_length=settings.DEFAULT_CHAR_FIELD_MAX_LENGTH,
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        verbose_name="Пост",
        related_name="comments",
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        related_name="comments",
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        default=datetime.utcnow,
    )

    objects = PostgresManager()

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
