from django.db.models import Sum
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from django.http import JsonResponse

from users.models import UserService

from .serializers import (
    UserServiceCreateSerialiser,
    UserServiceListSerializer,
    UserServiceRetrieveSerializer,
    UserHistoryPaymentSerializer,
    UserServiceUpdateSerialiser,
    ExpensesSerializer,
    ExpensesByCategorySerializer,
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


class ExpensesViewSet(viewsets.ModelViewSet):
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
        return UserService.objects.filter(
            user=self.request.user
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        ).aggregate(future_expenses=Sum('expense'))
        return JsonResponse(queryset)


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
