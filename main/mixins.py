from django.db import models
from django.utils import timezone
import uuid

class TimestampMixin(models.Model):
    """
    Абстрактный миксин, добавляющий поля даты создания и обновления.
    Позволяет не писать эти поля вручную в каждой модели проекта.
    """
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Создано',
        editable=False,
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """
    Миксин для замены стандартного целочисленного ID на UUID.
    Полезно для защиты от перебора (парсинга) ID в URL.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Миксин для мягкого удаления (soft delete).
    Вместо реального удаления из БД, запись помечается как неактивная.
    """
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True