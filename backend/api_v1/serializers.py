from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from services.models import Service, ServiceCategoryImage, CategoryImage
from users.models import UserService

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['accessToken'] = str(refresh.access_token)
        data['tokenType'] = "bearer"
        data['expiresIn'] = 28800
        data['refreshToken'] = str(refresh)

        del data['access']
        del data['refresh']

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class ServiceSerializer(serializers.ModelSerializer):
    serviceName = serializers.CharField(source='name')
    logo = serializers.ImageField(source='image_logo', use_url=True)
    subscriptionStatus = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = (
            'id',
            'logo',
            'serviceName',
            'cashback',
            'subscriptionStatus'
        )

    def get_subscriptionStatus(self, obj):
        if UserService.objects.filter(
            user=self.context.get('request').user,
            service=obj,
            is_active=1
        ).exists():
            return 1
        return 0


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


#class CreateUserServiceSerializer(serializers.ModelSerializer):

#    model = UserService
#    fields = (
#        'subscriptionId',
#        'phoneNumber'
#    )