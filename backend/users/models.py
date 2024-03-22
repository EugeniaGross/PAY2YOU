import uuid

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from services.models import Service, Tariff

User = get_user_model()


class UserPhoneNumber(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='phone_numbers'
    )
    phone_number = models.CharField(
        'Номер телефона',
        max_length=16,
        unique=True,
        validators=[
           RegexValidator(
               regex=r"^\+?1?\d{8,15}$"
           )
        ]
    )

    class Meta:
        verbose_name = 'номер телефона пользователя'
        verbose_name_plural = 'Номера телефона пользователя'


class UserService(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
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
        auto_now_add=True
    )
    end_date = models.DateField(
        'Дата окончания подписки на сервис'
    )
    is_active = models.PositiveSmallIntegerField(
        'Активность подписки'
    )
    auto_pay = models.BooleanField(
        'Автоплатеж',
        default=True
    )
    phone_number = models.OneToOneField(
        UserPhoneNumber,
        on_delete=models.CASCADE,
        verbose_name='Номер телефона',
        related_name='user_service'
    )

    class Meta:
        verbose_name = 'подписка пользователя'
        verbose_name_plural = 'Подписки пользователя'


class UserExpense(models.Model):
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
        related_name='user_expenses'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Сервис',
        related_name='user_expenses'
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name='Тариф',
        related_name='user_expenses'
    )
    date = models.DateField(
        'Дата',
        auto_now_add=True,
    )
    amount = models.PositiveSmallIntegerField(
        'Сумма'
    )

    class Meta:
        verbose_name = 'расходы пользователя'
        verbose_name_plural = 'Расходы пользователя'


class UserCashback(models.Model):
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
        related_name='user_cashback'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Сервис',
        related_name='user_cashback'
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name='Тариф',
        related_name='user_cashback'
    )
    date = models.DateField(
        'Дата',
        auto_now_add=True,
    )
    amount = models.PositiveSmallIntegerField(
        'Сумма'
    )

    class Meta:
        verbose_name = 'доходы пользователя'
        verbose_name_plural = 'Доходы пользователя'


class TrialPeriod(models.Model):
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
        'Дата начала',
        auto_now_add=True
    )
    end_date = models.DateField(
        'Дата завершения'
    )

    class Meta:
        verbose_name = 'пробный период'
        verbose_name_plural = 'Пробный период'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'service'],
                name='unique_user_service'
            )
        ]
