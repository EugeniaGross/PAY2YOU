from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from services.models import Service, ServiceCategoryImage, CategoryImage, Tariff, TariffCondition, TariffSpecialCondition
from users.models import UserService

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


class ServiceListSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(source='image_logo', use_url=True)
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = (
            'id',
            'logo',
            'name',
            'cashback',
            'is_subscribe'
        )

    def get_is_subscribe(self, obj):
        return UserService.objects.filter(
            user=self.context.get('request').user,
            service=obj,
            is_active=1
        ).exists()



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
        model=Tariff
        fields=(
            'id',
            'name',
            'trial_count',
            'trial_period',
            'price',
            'description'
        )


class TariffRetrieveSerializer(serializers.ModelSerializer):
    condition = serializers.SerializerMethodField()
    special_condition = serializers.SerializerMethodField()

    class Meta:
        model=Tariff
        fields=(
            'id',
            'name',
            'trial_count',
            'trial_period',
            'price',
            'description',
            'condition',
            'special_condition'
        )

    def get_condition(self, obj):
        return TarrifConditionSerializer(obj.tariff_conditions.all(), many=True).data


    def get_special_condition(self, obj):
        return TarrifSpecialConditionSerializer(obj.tariff_special_conditions.all(), many=True).data


class TarrifConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TariffCondition
        fields = (
            'count',
            'period',
            'price'
        )


class TarrifSpecialConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TariffSpecialCondition
        fields = (
            'count',
            'period',
            'price'
        )




#class CreateUserServiceSerializer(serializers.ModelSerializer):

#    model = UserService
#    fields = (
#        'subscriptionId',
#        'phoneNumber'
#    )