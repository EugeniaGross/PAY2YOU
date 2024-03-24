from datetime import timedelta

from rest_framework import serializers

from users.models import UserService, UserTrialPeriod
from ..utils import get_tariff_condition


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
        return obj.end_date + timedelta(days=1)


class UserServiceListSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(source='service.image_logo')
    service_name = serializers.CharField(source='service.name')
    tariff_name = serializers.CharField(source='tariff.name')
    price = serializers.IntegerField(source='expense')
    trial_period_end_date = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    payment_date = serializers.SerializerMethodField()
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
            'trial_period_end_date',
            'is_active'
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

    def get_is_active(self, obj):
        if obj.is_active == True and obj.auto_pay == True:
            return 1
        if obj.is_active == False and obj.auto_pay == False:
            return 0
        return 3

    def get_payment_date(self, obj):
        return obj.end_date + timedelta(days=1)

    def get_count(self, obj):
        return get_tariff_condition(
            obj,
            self.context['request'].user
        ).count

    def get_period(self, obj):
        return get_tariff_condition(
            obj,
            self.context['request'].user
        ).period
