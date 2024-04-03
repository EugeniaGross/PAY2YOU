from rest_framework import serializers

from services.models import (CategoryImage, Service, ServiceCategoryImage,
                             Tariff, TariffCondition, TariffSpecialCondition,
                             TariffTrialPeriod)

from ..utils import get_full_name_period


class ServiceListSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(source='image_logo', use_url=True)

    class Meta:
        model = Service
        fields = (
            'id',
            'logo',
            'name',
            'cashback'
        )


class ServiceRetrieveSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(source='image_logo', use_url=True)

    class Meta:
        model = Service
        fields = (
            'id',
            'name',
            'full_name',
            'short_description',
            'cashback',
            'logo',
            'description',
            'url'
        )


class CategoryImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryImage
        fields = (
            'id',
            'name'
        )


class ServiceCategoryImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceCategoryImage
        fields = (
            'id',
            'title',
            'image'
        )


class PopularServiceSerialiser(serializers.ModelSerializer):
    logo = serializers.ImageField(
        source='image_logo_popular',
        use_url=True
    )

    class Meta:
        model = Service
        fields = (
            'id',
            'logo',
            'cashback'
        )


class TariffListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tariff
        fields = (
            'id',
            'name',
            'description'
        )


class TariffRetrieveSerializer(serializers.ModelSerializer):
    condition = serializers.SerializerMethodField()
    special_condition = serializers.SerializerMethodField()
    trial_period = serializers.SerializerMethodField()

    class Meta:
        model = Tariff
        fields = (
            'id',
            'name',
            'description',
            'condition',
            'special_condition',
            'trial_period'
        )

    def get_condition(self, obj):
        return TariffConditionSerializer(
            obj.tariff_condition
        ).data

    def get_special_condition(self, obj):
        if TariffSpecialCondition.objects.filter(
            tariff=obj
        ).exists():
            return TariffSpecialConditionSerializer(
                obj.tariff_special_condition
            ).data
        return {}

    def get_trial_period(self, obj):
        if TariffTrialPeriod.objects.filter(
            tariff=obj
        ).exists():
            return TariffTrialPeriodSerializer(
                obj.tariff_trial_period
            ).data
        return {}


class TariffConditionSerializer(serializers.ModelSerializer):
    period = serializers.SerializerMethodField()

    class Meta:
        model = TariffCondition
        fields = (
            'count',
            'period',
            'price'
        )

    def get_period(self, obj):
        return get_full_name_period(obj.count, obj.period)


class TariffSpecialConditionSerializer(TariffConditionSerializer):

    class Meta(TariffConditionSerializer.Meta):
        model = TariffSpecialCondition


class TariffTrialPeriodSerializer(TariffConditionSerializer):

    class Meta(TariffConditionSerializer.Meta):
        model = TariffTrialPeriod
