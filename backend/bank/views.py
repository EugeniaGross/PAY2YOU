from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .response_shema import response_schema_dict, response_schema_dict_cashback

User = get_user_model()


@swagger_auto_schema(
    method='post',
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
@api_view(['POST'])
@permission_classes((AllowAny, ))
def payment(request):
    if User.objects.filter(email=request.data['user']).exists():
        return Response(
            {'message': 'Оплата прошла'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Оплата не прошла'},
        status=status.HTTP_400_BAD_REQUEST
    )


@swagger_auto_schema(
    method='post',
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
@api_view(['POST'])
@permission_classes((AllowAny, ))
def cashback_accrual(request):
    if User.objects.filter(email=request.data['user']).exists():
        return Response(
            {'message': 'Кэшбек начислен'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Кэшбек не зачислен'},
        status=status.HTTP_400_BAD_REQUEST
    )
