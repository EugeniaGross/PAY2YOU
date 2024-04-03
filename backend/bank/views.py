from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


@api_view(['POST'])
def create_payment(request):
    """
    Так как приложение не знает банковской карты пользователя,
    и пользователь вводит свой номер телефона только при создании
    подписки, а в БД приложения номер телефона сохраняется только после
    подключения подписки, сделали самую простую логику.
    """
    if request.data['user'] in User.objects.all():
        return Response(
            {'message': 'Оплата прошла'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Оплата не прошла'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def get_cashback(request):
    if request.data['user'] in User.objects.all():
        return Response(
            {'message': 'Кэшбек начислен'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Кэшбек не зачислен'},
        status=status.HTTP_400_BAD_REQUEST
    )
