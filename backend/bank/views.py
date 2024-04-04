from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny

from .response_shema import response_schema_dict, response_schema_dict_cashback

User = get_user_model()


class PaymentViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        operation_description=(
            'Совершение платежа.'
        ),
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                ),
                'price': openapi.Schema(
                    type=openapi.TYPE_INTEGER
                )
            }
        ),
        responses=response_schema_dict
    )
    def create(self, request, *args, **kwargs):
        if User.objects.filter(email=request.data['user']).exists():
            return Response(
                {'message': 'Оплата прошла'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'Оплата не прошла'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CashbackViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        operation_description=(
            'Совершение платежа.'
        ),
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                ),
                'price': openapi.Schema(
                    type=openapi.TYPE_INTEGER
                )
            }
        ),
        responses=response_schema_dict_cashback
    )
    def create(self, request, *args, **kwargs):
        if User.objects.filter(email=request.data['user']).exists():
            return Response(
                {'message': 'Кэшбек начислен'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'Кэшбек не зачислен'},
            status=status.HTTP_400_BAD_REQUEST
        )
