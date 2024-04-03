# Generated by Django 3.2.16 on 2024-04-02 13:27

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=250, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'категория изображений',
                'verbose_name_plural': 'Категории изображений',
            },
        ),
        migrations.CreateModel(
            name='CategoryService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'категория сервисов',
                'verbose_name_plural': 'Категории сервисов',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=250, verbose_name='Название сервиса')),
                ('full_name', models.CharField(max_length=250, verbose_name='Полное название сервиса')),
                ('short_description', models.CharField(max_length=250, verbose_name='Короткое описание')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image_logo', models.ImageField(upload_to='images_logo/', verbose_name='Логотип')),
                ('image_logo_popular', models.ImageField(upload_to='images_logo/', verbose_name='Логотип для категории популярные сервисы')),
                ('image_logo_poster', models.ImageField(upload_to='images_logo/', verbose_name='Постер')),
                ('cashback', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100, message='Значение не может быть больше 100')], verbose_name='Кэшбек')),
                ('url', models.URLField(verbose_name='Ссылка на сервис')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.categoryservice', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'сервис',
                'verbose_name_plural': 'Сервисы',
            },
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=250, verbose_name='Название трифа')),
                ('description', models.TextField(verbose_name='Описание тарифа')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tariffs', to='services.service', verbose_name='Сервис')),
            ],
            options={
                'verbose_name': 'тариф',
                'verbose_name_plural': 'Тарифы',
            },
        ),
        migrations.CreateModel(
            name='TariffTrialPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField(verbose_name='Количество пробных дней/месяцев/лет')),
                ('period', models.CharField(choices=[('D', 'Day'), ('M', 'Month'), ('Y', 'Year')], max_length=250, verbose_name='Пробный период (день, месяц, год)')),
                ('price', models.PositiveSmallIntegerField(verbose_name='Цена пробного периода')),
                ('tariff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tariff_trial_period', to='services.tariff', verbose_name='Тариф')),
            ],
            options={
                'verbose_name': 'пробный период тарифа',
                'verbose_name_plural': 'Пробный период тарифа',
            },
        ),
        migrations.CreateModel(
            name='TariffSpecialCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField(verbose_name='Количество дней/месяцев/лет')),
                ('period', models.CharField(choices=[('D', 'Day'), ('M', 'Month'), ('Y', 'Year')], max_length=250, verbose_name='Период (день, месяц, год)')),
                ('price', models.PositiveIntegerField()),
                ('tariff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tariff_special_condition', to='services.tariff', verbose_name='Тариф')),
            ],
            options={
                'verbose_name': 'специальное условие тарифа',
                'verbose_name_plural': 'Специальное условия тарифа',
            },
        ),
        migrations.CreateModel(
            name='TariffCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество не может быть меньше 1')], verbose_name='Количество дней/месяцев/лет')),
                ('period', models.CharField(choices=[('D', 'Day'), ('M', 'Month'), ('Y', 'Year')], max_length=250, verbose_name='Период (день, месяц, год)')),
                ('price', models.PositiveIntegerField()),
                ('tariff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tariff_condition', to='services.tariff', verbose_name='Тариф')),
            ],
            options={
                'verbose_name': 'условие тарифа',
                'verbose_name_plural': 'Условие тарифа',
            },
        ),
        migrations.CreateModel(
            name='ServiceCategoryImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок к изображению')),
                ('image', models.ImageField(upload_to='image_category/', verbose_name='Избражение')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_category_images', to='services.categoryimage', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'изображение для сервиса',
                'verbose_name_plural': 'Изображения для сервиса',
            },
        ),
        migrations.AddField(
            model_name='categoryimage',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_images', to='services.service', verbose_name='Сервис'),
        ),
    ]
