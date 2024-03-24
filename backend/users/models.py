import uuid

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from services.models import Service, Tariff

User = get_user_model()


class UserService(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_services'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Сервис',
        related_name='user_services'
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name='Тариф',
        related_name='user_services'
    )
    start_date = models.DateField(
        'Дата начала подписки на сервис',
    )
    end_date = models.DateField(
        'Дата окончания подписки на сервис'
    )
    expense = models.PositiveSmallIntegerField(
        'Сумма'
    )
    cashback = models.PositiveSmallIntegerField(
        'Кэшбек'
    )
    status_cashback = models.BooleanField(
        'Статус зачисления кэшбека'
    )
    is_active = models.BooleanField(
        'Активность подписки'
    )
    auto_pay = models.BooleanField(
        'Автоплатеж',
        default=True
    )
    phone_number = models.CharField(
        'Номер телефона',
        max_length=16,
        validators=[
           RegexValidator(
               regex=r"^\+?1?\d{8,15}$"
           )
        ]
    )

    class Meta:
        verbose_name = 'подписка пользователя'
        verbose_name_plural = 'Подписки пользователя'


class UserTrialPeriod(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='trial_period'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Сервис',
        related_name='trial_period'
    )
    start_date = models.DateField(
        'Дата начала'
    )
    end_date = models.DateField(
        'Дата завершения'
    )

    class Meta:
        verbose_name = 'пробный период пользователя'
        verbose_name_plural = 'Пробный период пользователя'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'service'],
                name='unique_user_service'
            )
        ]


class UserSpecialCondition(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='special_conditions'
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name='Тариф',
        related_name='special_conditions'
    )
    start_date = models.DateField(
        'Дата начала'
    )
    end_date = models.DateField(
        'Дата завершения'
    )

    class Meta:
        verbose_name = 'специальное условие для пользователя'
        verbose_name_plural = 'Специальные условия для пользователя'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'tariff'],
                name='unique_user_tariff'
            )
        ]
