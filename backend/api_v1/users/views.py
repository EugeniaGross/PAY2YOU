from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

from users.models import UserService

from .serializers import UserServiceListSerializer, UserServiceRetrieveSerializer, UserHistoryPaymentSerializer
from ..filters import UserServiceFilter, UserServiceDateFilter, FutureExpensesSerializer, ExpensesByCategorySerializer
from ..pagination import ServicePagination


class UserServiceViewSet(viewsets.ModelViewSet):
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
