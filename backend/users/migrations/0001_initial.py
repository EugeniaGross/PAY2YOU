# Generated by Django 3.2.15 on 2024-03-23 19:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTrialPeriod',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата завершения')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trial_period', to='services.service', verbose_name='Сервис')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trial_period', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'пробный период пользователя',
                'verbose_name_plural': 'Пробный период пользователя',
            },
        ),
        migrations.CreateModel(
            name='UserSpecialCondition',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата завершения')),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_conditions', to='services.tariff', verbose_name='Тариф')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_conditions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'специальное условие для пользователя',
                'verbose_name_plural': 'Специальные условия для пользователя',
            },
        ),
        migrations.CreateModel(
            name='UserService',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start_date', models.DateField(verbose_name='Дата начала подписки на сервис')),
                ('end_date', models.DateField(verbose_name='Дата окончания подписки на сервис')),
                ('is_active', models.BooleanField(verbose_name='Активность подписки')),
                ('auto_pay', models.BooleanField(default=True, verbose_name='Автоплатеж')),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Номер телефона')),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_services', to='services.tariff', verbose_name='Тариф')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_services', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'подписка пользователя',
                'verbose_name_plural': 'Подписки пользователя',
            },
        ),
        migrations.CreateModel(
            name='UserExpense',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField(verbose_name='Дата')),
                ('expense', models.PositiveSmallIntegerField(verbose_name='Сумма')),
                ('cashback', models.PositiveSmallIntegerField(verbose_name='Кэшбек')),
                ('status_cashback', models.BooleanField(verbose_name='Статус зачисления кэшбека')),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_expenses', to='services.tariff', verbose_name='Тариф')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_expenses', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'расходы и кэшбек пользователя',
                'verbose_name_plural': 'Расходы и кэшбек пользователя',
            },
        ),
        migrations.AddConstraint(
            model_name='usertrialperiod',
            constraint=models.UniqueConstraint(fields=('user', 'service'), name='unique_user_service'),
        ),
        migrations.AddConstraint(
            model_name='userspecialcondition',
            constraint=models.UniqueConstraint(fields=('user', 'tariff'), name='unique_user_tariff'),
        ),
    ]
