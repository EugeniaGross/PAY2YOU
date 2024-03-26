from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets

from users.models import UserService

from .serializers import (
    UserServiceCreateSerialiser,
    UserServiceListSerializer,
    UserServiceRetrieveSerializer,
    UserHistoryPaymentSerializer,
    UserServiceUpdateSerialiser,
    FutureExpensesSerializer,
    ExpensesByCategorySerializer
)
from ..filters import UserServiceFilter, UserServiceDateFilter
from ..mixins import UpdateModelMixin
from ..pagination import ServicePagination


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


class ExpensesByCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ExpensesByCategorySerializer
    queryset = UserService.objects.all()[:1]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {'start_date': self.request.GET.get('start_date'),
             'end_date': self.request.GET.get('end_date')}
        )
        return context


class FutureExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = FutureExpensesSerializer
    queryset = UserService.objects.all()[:1]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {'start_date': self.request.GET.get('start_date'),
             'end_date': self.request.GET.get('end_date')}
        )
        return context


class CashbackViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserServiceDateFilter

    def get_queryset(self):
        return UserService.objects.filter(
            user=self.request.user
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        ).aggregate(cashback=Sum('cashback'))
        return JsonResponse(queryset)
