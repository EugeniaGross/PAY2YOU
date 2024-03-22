import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

CHOICES = (
        ('D', 'Дней'),
        ('M', 'Месяцев'),
        ('Y', 'Год'),
    )


class CategoryService(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=250
    )


class Service(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        'Название сервиса',
        max_length=250
    )
    full_name = models.CharField(
        'Полное название сервиса',
        max_length=250
    )
    short_description = models.CharField(
        'Короткое описание',
        max_length=250
    )
    description = models.TextField(
        'Описание'
    )
    image_logo = models.ImageField(
        'Логотип',
        upload_to='images_logo/'
    )
    image_logo_popular = models.ImageField(
        'Логотип для категории популярные сервисы',
        upload_to='images_logo/'
    )
    image_logo_poster = models.ImageField(
        'Постер',
        upload_to='images_logo/'
    )
    cashback = models.PositiveSmallIntegerField(
        'Кэшбек',
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(
                100,
                message='Значение не может быть больше 100'
            )
        ]
    )
    category = models.ForeignKey(
        CategoryService,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='services'
    )

    class Meta:
        verbose_name = 'сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.name


class Tariff(models.Model):
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
        related_name='tariffs'
    )
    name = models.CharField(
        'Название трифа',
        max_length=250
    )
    description = models.TextField(
        'Описание тарифа'
    )
    trial_count = models.PositiveSmallIntegerField(
        'Количество пробных дней/месяцев/лет',
        blank=True,
        null=True
    )
    trial_period = models.CharField(
        'Пробный период (день, месяц, год)',
        max_length=250,
        choices = CHOICES
    )

    class Meta:
        verbose_name = 'тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.name


class TarrifCondition(models.Model):
    tarrif = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name='Условия тарифа',
        related_name='tariff_conditions'
    )
    count = models.PositiveSmallIntegerField(
        'Количество дней/месяцев/лет',
        validators=[
            MinValueValidator(
                1,
                message='Количество не может быть меньше 1'
            )
        ]
    )
    period = models.CharField(
        'Период (день, месяц, год)',
        max_length=250,
        choices = CHOICES
    )
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'условие тарифа'
        verbose_name_plural = 'Условия тарифа'


class TariffSpecialCondition(models.Model):
    tarrif = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        verbose_name='Условия тарифа',
        related_name='tariff_special_conditions'
    )
    count = models.PositiveSmallIntegerField(
        'Количество дней/месяцев/лет'
    )
    period = models.CharField(
        'Период (день, месяц, год)',
        max_length=250,
        choices = CHOICES
    )
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'специальное условие тарифа'
        verbose_name_plural = 'Специальные условия тарифа'


class CategoryImage(models.Model):
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
        related_name='category_images'
    )
    name = models.CharField(
        'Название категории',
        max_length=250
    )

    class Meta:
        verbose_name = 'категория изображений'
        verbose_name_plural = 'Категории изображений'

    def __str__(self):
        return self.name


class ServiceCategoryImage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    category = models.ForeignKey(
        CategoryImage,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='service_category_images'
    )
    image = models.ImageField(
        'Избражение',
        upload_to='image_category/'
    )

    class Meta:
        verbose_name = 'изображение для сервиса'
        verbose_name_plural = 'Изображения для сервиса'
