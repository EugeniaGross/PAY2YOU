from datetime import datetime, timedelta
from re import search

from django.contrib.auth.models import update_last_login
from django.urls import reverse
from requests import post
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from services.models import TariffSpecialCondition, TariffTrialPeriod
from users.models import UserService, UserSpecialCondition, UserTrialPeriod

from ..exeptions import PaymentError
from ..utils import (connect_special_condition, create_subscribe, get_days,
                     get_full_name_period, get_past_expenses_category,
                     get_tariff_condition)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['access'] = str(refresh.access_token)
        data['type'] = "Bearer"
        data['validity_period'] = 28800
        data['refresh'] = str(refresh)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserServiceRetrieveSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(source='service.image_logo_poster')
    service_name = serializers.CharField(source='service.name')
    cashback = serializers.IntegerField(source='service.cashback')
    tariff_name = serializers.CharField(source='tariff.name')
    price = serializers.IntegerField(source='expense')
    trial_period_end_date = serializers.SerializerMethodField()
    payment_date = serializers.SerializerMethodField()

    class Meta:
        model = UserService
        fields = (
            'id',
            'logo',
            'service_name',
            'tariff_name',
            'cashback',
            'payment_date',
            'end_date',
            'trial_period_end_date',
            'phone_number',
            'price'
        )

    def get_trial_period_end_date(self, obj):
        if UserTrialPeriod.objects.filter(
            user=obj.user,
            service=obj.service
        ).exists():
            return obj.service.trial_period.get(
                user=self.context['request'].user
            ).end_date
        return ''

    def get_payment_date(self, obj):
        if obj.end_date >= datetime.now().date() and obj.auto_pay:
            return obj.end_date + timedelta(days=1)
        return ''


class UserServiceListSerializer(UserServiceRetrieveSerializer):
    logo = serializers.ImageField(source='service.image_logo')
    is_active = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    period = serializers.SerializerMethodField()

    class Meta:
        model = UserService
        fields = (
            'id',
            'logo',
            'service_name',
            'tariff_name',
            'count',
            'period',
            'price',
            'payment_date',
            'end_date',
            'trial_period_end_date',
            'is_active'
        )

    def get_is_active(self, obj):
        if obj.is_active and obj.auto_pay:
            return 1
        if not obj.is_active and not obj.auto_pay:
            return 0
        return 3

    def get_count(self, obj):
        return get_tariff_condition(
            obj,
            self.context['request'].user
        ).count

    def get_period(self, obj):
        period = get_tariff_condition(
            obj,
            self.context['request'].user
        ).period
        count = self.get_count(obj)
        return get_full_name_period(count, period)


class UserServiceCreateSerialiser(serializers.ModelSerializer):

    class Meta:
        model = UserService
        fields = (
            'tariff',
            'phone_number'
        )

    def validate(self, attrs):
        phone_number = search(r'^\+79[0-9]{9}$', attrs['phone_number'])
        if not phone_number:
            raise serializers.ValidationError(
                'Введите корректный номер телефона'
            )
        if UserService.objects.filter(
            user=self.context['request'].user,
            tariff=attrs['tariff'],
            phone_number=attrs['phone_number']
        ).exists():
            raise serializers.ValidationError(
                'Вы уже были подписаны на этот сервис и тариф'
            )
        return super().validate(attrs)

    def create(self, validated_data):
        url = reverse('payment')
        if (TariffTrialPeriod.objects.filter(
                tariff=validated_data['tariff']
            ).exists()
            and not UserTrialPeriod.objects.filter(
                user=self.context['request'].user,
                service=validated_data['tariff'].service
        ).exists()
        ):
            response = post(
                url,
                data={
                    'user': self.context['request'].user,
                    'price': validated_data['tariff'].tariff_trial_period.price
                }
            )
            if response.status_code != 200:
                raise PaymentError
            days = get_days(validated_data['tariff'].tariff_trial_period)
            user_service = UserService.objects.create(
                user=self.context['request'].user,
                service=validated_data['tariff'].service,
                tariff=validated_data['tariff'],
                start_date=datetime.now().date(),
                end_date=datetime.now().date() + timedelta(days=days),
                expense=validated_data['tariff'].tariff_trial_period.price,
                cashback=0,
                is_active=True,
                auto_pay=True,
                status_cashback=False,
                phone_number=validated_data['phone_number']
            )
            UserTrialPeriod.objects.create(
                user=self.context['request'].user,
                service=validated_data['tariff'].service,
                start_date=datetime.now().date(),
                end_date=datetime.now().date() + timedelta(days=days)
            )
            return user_service
        if TariffSpecialCondition.objects.filter(
            tariff=validated_data['tariff']
        ).exists()\
            and not UserSpecialCondition.objects.filter(
                user=self.context['request'].user,
                tariff=validated_data['tariff']
        ).exists():
            price = validated_data['tariff'].tariff_special_condition.price
            response = post(
                url,
                data={
                    'user': self.context['request'].user,
                    'price': price
                }
            )
            if response.status_code != 200:
                raise PaymentError
            days = get_days(object.tariff_special_condition)
            return connect_special_condition(
                object=validated_data['tariff'],
                days=days,
                user=self.context['request'].user,
                phone_number=validated_data['phone_number']
            )
        response = post(
            url,
            data={
                'user': self.context['request'].user,
                'price': validated_data['tariff'].tariff_condition.price
            }
        )
        if response.status_code != 200:
            raise PaymentError
        days = get_days(validated_data['tariff'].tariff_condition)
        return create_subscribe(
            object=validated_data['tariff'],
            days=days,
            user=self.context['request'].user,
            phone_number=validated_data['phone_number']
        )

    def to_representation(self, instance):
        return UserServiceRetrieveSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class UserServiceUpdateSerialiser(serializers.ModelSerializer):

    class Meta:
        model = UserService
        fields = (
            'auto_pay',
        )

    def validate(self, attrs):
        if (attrs['auto_pay']
            and UserService.objects.filter(
                user=self.context['request'].user,
                tariff=self.instance.tariff,
                is_active=True,
                auto_pay=True
        ).exists()
        ):
            raise serializers.ValidationError(
                'Подписка уже возобновлена'
            )
        return super().validate(attrs)

    def update(self, instance, validated_data):
        if instance.end_date < datetime.now().date()\
           and validated_data['auto_pay']:
            url = reverse('payment')
            if TariffSpecialCondition.objects.filter(
                tariff=instance.tariff
            ).exists()\
                and not UserSpecialCondition.objects.filter(
                    user=self.context['request'].user,
                    tariff=instance.tariff
            ).exists():
                price = validated_data['tariff'].tariff_special_condition.price
                response = post(
                    url,
                    data={
                        'user': self.context['request'].user,
                        'price': price
                    }
                )
                if response.status_code != 200:
                    raise PaymentError
                days = get_days(instance.tariff.tariff_special_condition)
                return connect_special_condition(
                    object=instance.tariff,
                    days=days,
                    user=instance.user,
                    phone_number=instance.phone_number
                )
            price = validated_data['tariff'].tariff_condition.price
            response = post(
                url,
                data={
                    'user': self.context['request'].user,
                    'price': price
                }
            )
            if response.status_code != 200:
                raise PaymentError
            days = get_days(instance.tariff.tariff_condition)
            return create_subscribe(
                object=instance.tariff,
                days=days,
                user=instance.user,
                phone_number=instance.phone_number
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return UserServiceRetrieveSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class UserHistoryPaymentSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(source='service.image_logo')
    service_name = serializers.CharField(source='service.name')
    tariff_name = serializers.CharField(source='tariff.name')
    price = serializers.IntegerField(source='expense')
    date = serializers.DateField(source='start_date')

    class Meta:
        model = UserService
        fields = (
            'id',
            'logo',
            'service_name',
            'tariff_name',
            'cashback',
            'price',
            'status_cashback',
            'date'
        )


class ExpensesSerializer(serializers.ModelSerializer):
    expenses = serializers.SerializerMethodField()

    class Meta:
        model = UserService
        fields = ('expenses',)

    def get_expenses(self, obj):
        total = 0
        for expense in get_past_expenses_category(obj, self.context):
            total += expense.get('expenses')
        return total


class ExpensesByCategorySerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = UserService
        fields = ('data',)

    def get_data(self, obj):
        expenses = get_past_expenses_category(obj, self.context)
        for expense in expenses:
            del expense['service__category__name']
        return expenses
