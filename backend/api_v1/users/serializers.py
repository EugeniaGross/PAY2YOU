from datetime import datetime, timedelta
from math import floor
from re import search

from rest_framework import serializers

from services.models import TariffTrialPeriod, TariffSpecialCondition
from users.models import UserService, UserTrialPeriod, UserSpecialCondition
from ..utils import get_tariff_condition, get_days, get_full_name_period, get_past_expenses_category


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
        if obj.end_date >= datetime.now().date() and obj.auto_pay == True:
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
        if obj.is_active == True and obj.auto_pay == True:
            return 1
        if obj.is_active == False and obj.auto_pay == False:
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
        if (TariffTrialPeriod.objects.filter(
                tariff=validated_data['tariff']
            ).exists()
            and not UserTrialPeriod.objects.filter(
                user=self.context['request'].user,
                service=validated_data['tariff'].service
        ).exists()
        ):
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
        if (TariffSpecialCondition.objects.filter(
                tariff=validated_data['tariff']
            ).exists()
            and not UserSpecialCondition.objects.filter(
                user=self.context['request'].user,
                tariff=validated_data['tariff']
        ).exists()
        ):
            days = get_days(validated_data['tariff'].tariff_special_condition)
            user_service = UserService.objects.create(
                user=self.context['request'].user,
                service=validated_data['tariff'].service,
                tariff=validated_data['tariff'],
                start_date=datetime.now().date(),
                end_date=datetime.now().date() + timedelta(days=days),
                expense=validated_data['tariff'].tariff_special_condition.price,
                cashback=0,
                is_active=True,
                auto_pay=True,
                status_cashback=False,
                phone_number=validated_data['phone_number']
            )
            UserSpecialCondition.objects.create(
                user=self.context['request'].user,
                tariff=validated_data['tariff'],
                start_date=datetime.now().date(),
                end_date=datetime.now().date() + timedelta(days=days)
            )
            return user_service
        days = get_days(validated_data['tariff'].tariff_condition)
        price = validated_data['tariff'].tariff_condition.price
        cashback = validated_data['tariff'].service.cashback
        return UserService.objects.create(
            user=self.context['request'].user,
            service=validated_data['tariff'].service,
            tariff=validated_data['tariff'],
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=days),
            expense=validated_data['tariff'].tariff_condition.price,
            cashback=floor(price * cashback / 100),
            is_active=True,
            auto_pay=True,
            status_cashback=False,
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
            'is_active',
            'auto_pay'
        )

    def validate(self, attrs):
        if (attrs['auto_pay'] == True
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
        if instance.end_date < datetime.now().date() and validated_data['auto_pay'] == True:
            if (TariffSpecialCondition.objects.filter(
                    tariff=instance.tariff
                ).exists()
                and not UserSpecialCondition.objects.filter(
                    user=self.context['request'].user,
                    tariff=instance.tariff
            ).exists()
            ):
                days = get_days(instance.tariff.tariff_special_condition)
                instance = UserService.objects.create(
                    user=self.instance.user,
                    service=instance.service,
                    tariff=instance.tariff,
                    start_date=datetime.now().date(),
                    end_date=datetime.now().date() + timedelta(days=days),
                    expense=instance.tariff.tariff_special_condition.price,
                    cashback=0,
                    is_active=True,
                    auto_pay=True,
                    status_cashback=False,
                    phone_number=instance.phone_number
                )
                UserSpecialCondition.objects.create(
                    user=self.context['request'].user,
                    tariff=instance.tariff,
                    start_date=datetime.now().date(),
                    end_date=datetime.now().date() + timedelta(days=days)
                )
                return instance
            days = get_days(instance.tariff.tariff_condition)
            price = instance.tariff.tariff_condition.price
            cashback = instance.tariff.service.cashback
            return UserService.objects.create(
                user=instance.user,
                service=instance.tariff.service,
                tariff=instance.tariff,
                start_date=datetime.now().date(),
                end_date=datetime.now().date() + timedelta(days=days),
                expense=instance.tariff.tariff_condition.price,
                cashback=floor(price * cashback / 100),
                is_active=True,
                auto_pay=True,
                status_cashback=False,
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
