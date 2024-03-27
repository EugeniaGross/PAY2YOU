from datetime import date
from calendar import monthrange

from django.db.models import Sum, F
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import UserService

from .serializers import (
    UserServiceCreateSerialiser,
    UserServiceListSerializer,
    UserServiceRetrieveSerializer,
    UserHistoryPaymentSerializer,
    UserServiceUpdateSerialiser,
    ExpensesByCategorySerializer,
    CustomTokenObtainPairSerializer,
    ExpensesSerializer
)
from ..filters import UserServiceFilter, UserServiceDateFilter
from ..mixins import UpdateModelMixin
from ..pagination import ServicePagination


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description=(
            'Возвращает токен, тип токена и время жизни в '
            'секундах.'
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    'type': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    'validity_period': openapi.Schema(
                        type=openapi.TYPE_INTEGER
                    ),
                    'refresh': openapi.Schema(
                        type=openapi.TYPE_STRING
                    )
                }
            )
        }
    )
    def post(self, request: Request, *args, **kwargs) -> mixins.Response:
        return super().post(request, *args, **kwargs)


class UserServiceViewSet(UpdateModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = ServicePagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = UserServiceFilter

    def get_queryset(self):
        return UserService.objects.filter(
            user=self.request.user
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return UserServiceListSerializer
        if self.action == 'create':
            return UserServiceCreateSerialiser
        if self.action == 'partial_update':
            return UserServiceUpdateSerialiser
        return UserServiceRetrieveSerializer

    @swagger_auto_schema(
        operation_description=(
            'Возвращает список подписок пользователя. '
            'При использовании в параметре is_active=1 '
            'возвращает список активных подписок, при использовании '
            'is_active=0 список неактивных подписок.'
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'logo': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'service_name': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'tariff_name': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'count': openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                ),
                                'period': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'price': openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                ),
                                'payment_date': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'end_date': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'trial_period_end_date': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'is_active': openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                ),
                            }
                        )
                    ),
                    'next': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    'previous': openapi.Schema(
                        type=openapi.TYPE_STRING
                    )
                }
            )
        }

    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Возвращает информацию о подписке пользователя. '
        )
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Подключение подписки. Для подключения подписки '
            'необходимо в теле запроса передать id тарифа и '
            'и номер телефона пользователя. Пользователь может '
            'подключить этот тариф только один раз. При отключении '
            'подписки он сможет ее возобновить.'
        ),
        responses={status.HTTP_200_OK: UserServiceRetrieveSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Отключение и возобновление подписки. Для отключения подписки '
            'необходимо в теле запроса auto_pay=False. Для возобновления '
            'auto_pay=False. Если при возобновлении срок действия подписки '
            'окончен, создается новый экземпляр подписки.'
        ),
        responses={status.HTTP_200_OK: UserServiceRetrieveSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class UserHistoryPaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserHistoryPaymentSerializer
    pagination_class = ServicePagination
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = UserServiceDateFilter
    ordering = ('-start_date',)

    def get_queryset(self):
        return UserService.objects.filter(
            user=self.request.user
        )

    @swagger_auto_schema(
        operation_description=(
            'Список платежей пользователя '
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'logo': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'service_name': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'tariff_name': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'cashback': openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                ),
                                'price': openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                ),
                                'status_cashback': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN
                                ),
                                'date': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                            }
                        )
                    ),
                    'next': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    'previous': openapi.Schema(
                        type=openapi.TYPE_STRING
                    )
                }
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Детали оплаты подписки пользователя '
        )
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ExpensesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ExpensesSerializer
    queryset = UserService.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {'start_date': self.request.GET.get('start_date'),
             'end_date': self.request.GET.get('end_date')}
        )
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        return Response(serializer.data)


class ExpensesByCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ExpensesByCategorySerializer
    queryset = UserService.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {'start_date': self.request.GET.get('start_date'),
             'end_date': self.request.GET.get('end_date')}
        )
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        return Response(serializer.data)


class FutureExpensesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        last_day = monthrange(date.today().year, date.today().month)[1]
        last_current_month_date = date(
            date.today().year, date.today().month, last_day)
        queryset = UserService.objects.filter(
            user=self.request.user,
            is_active=1,
            auto_pay=1,
            end_date__gt=date.today(),
            end_date__lt=last_current_month_date,
        )
        return queryset

    def list(self, request, *args, **kwargs):
        expense = {}
        queryset = self.get_queryset()
        special_condition_expense = queryset.filter(
            tariff__tariff_trial_period__tariff_id=F('tariff'),
            service__trial_period__end_date=F('end_date'),
            tariff__tariff_special_condition__tariff_id=F('tariff'),
        )
        non_special_condition_expense = queryset.difference(
            special_condition_expense)

        expense = special_condition_expense.aggregate(
            future_expenses=Sum('tariff__tariff_special_condition__price'))
        for value in non_special_condition_expense.values(
            'tariff__tariff_condition__price'
        ):
            expense['future_expenses'] = expense.get(
                'future_expenses', 0) + list(value.values())[0]

        return JsonResponse(expense)


class CashbackViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserServiceDateFilter

    def get_queryset(self):
        return UserService.objects.filter(
            user=self.request.user
        )

    @swagger_auto_schema(
        operation_description=(
            'Возвращает сколько всего кэшбека заработал пользователь '
            'за время использования приложения PAY2YOU. '
            'При использовании параметров запроса start_date и end_date '
            'возвращает сумму кэшбека за период.'
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'cashback': openapi.Schema(
                        type=openapi.TYPE_INTEGER
                    )
                }
            )
        }
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        ).aggregate(cashback=Sum('cashback'))
        return JsonResponse(queryset)
