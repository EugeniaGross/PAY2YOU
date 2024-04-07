from calendar import monthrange
from collections import Counter
from datetime import date

from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import UserService

from ..filters import UserServiceDateFilter, UserServiceFilter
from ..mixins import UpdateModelMixin
from ..pagination import ServicePagination
from ..permissions import IsAuthorOrReadOnly
from .serializers import (CustomTokenObtainPairSerializer,
                          ExpensesByCategorySerializer, ExpensesSerializer,
                          UserHistoryPaymentSerializer,
                          UserServiceCreateSerialiser,
                          UserServiceListSerializer,
                          UserServiceRetrieveSerializer,
                          UserServiceUpdateSerialiser)


class CustomUserViewSet(UserViewSet):
    @swagger_auto_schema(
        operation_description=(
            'Регистрация пользователя по адресу электроной '
            'почты и паролю.'
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    'email': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                }
            ),
            status.HTTP_400_BAD_REQUEST: "BAD REQUEST"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


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
            ),
            status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED"
        }
    )
    def post(self, request: Request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserServiceViewSet(
    UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pagination_class = ServicePagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = UserServiceFilter
    permission_classes = (IsAuthorOrReadOnly, )

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
            ),
            status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Возвращает информацию о подписке пользователя. '
        ),
        responses={
            status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
            status.HTTP_404_NOT_FOUND: "NOT_FOUND"
        }
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
        responses={
            status.HTTP_200_OK: UserServiceRetrieveSerializer,
            status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
            status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
            status.HTTP_404_NOT_FOUND: "NOT_FOUND"
        }
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
        responses={status.HTTP_200_OK: UserServiceRetrieveSerializer,
                   status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
                   status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
                   status.HTTP_403_FORBIDDEN: "FORBIDDEN",
                   status.HTTP_404_NOT_FOUND: "NOT_FOUND"
                   }
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

    @swagger_auto_schema(
        operation_description=(
            'Возвращает расходы за выбранный период '
            'за время использования приложения PAY2YOU. '
            'Период задается параметрами запроса start_date и end_date. '
        ),
        manual_parameters=[
            openapi.Parameter(
                "start_date",
                openapi.IN_PATH,
                description=("Дата начала периода"),
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_PATH,
                description=("Дата окончания периода"),
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'expenses': openapi.Schema(
                        type=openapi.TYPE_INTEGER
                    )
                }
            ),
            status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
            status.HTTP_404_NOT_FOUND: "NOT_FOUND"
        }
    )
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


class ExpensesByCategoryViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ExpensesByCategorySerializer
    queryset = UserService.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {'start_date': self.request.GET.get('start_date'),
             'end_date': self.request.GET.get('end_date')}
        )
        return context

    @swagger_auto_schema(
        operation_description=(
            'Возвращает расходы за выбранный период, отсортированные '
            'по категориям за время использования приложения PAY2YOU. '
            'Период задается параметрами запроса start_date и end_date. '
        ),
        manual_parameters=[
            openapi.Parameter(
                "start_date",
                openapi.IN_PATH,
                description=("Дата начала периода"),
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_PATH,
                description=("Дата окончания периода"),
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'expenses': openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                )
                            }
                        )
                    )
                }
            ),
            status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED"
        }
    )
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
            end_date__lte=last_current_month_date,
        )
        return queryset

    @swagger_auto_schema(
        operation_description=(
            'Возвращает предстоящие затраты пользователя '
            'на подписки в текущем месяце.  '
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'future_expenses': openapi.Schema(
                        type=openapi.TYPE_INTEGER
                    )
                }
            ),
            status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
            status.HTTP_404_NOT_FOUND: "NOT_FOUND"
        }
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        special_condition_expense = queryset.filter(
            tariff__tariff_trial_period__tariff_id=F('tariff'),
            service__trial_period__end_date=F('end_date'),
            tariff__tariff_special_condition__tariff_id=F('tariff'),
        )
        non_special_condition_expense = queryset.exclude(
            tariff__tariff_trial_period__tariff_id=F('tariff'),
            service__trial_period__end_date=F('end_date'),
            tariff__tariff_special_condition__tariff_id=F('tariff'),
        )

        expense = special_condition_expense.aggregate(
            future_expenses=Coalesce(Sum('tariff__tariff_special_condition__price'), 0))
        expense2 = non_special_condition_expense.aggregate(
            future_expenses=Coalesce(Sum('tariff__tariff_condition__price'), 0))
        expense = dict(Counter(expense) + Counter(expense2))

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
            ),
            status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
            status.HTTP_404_NOT_FOUND: "NOT_FOUND"
        }
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        ).aggregate(cashback=Sum('cashback'))
        return JsonResponse(queryset)
