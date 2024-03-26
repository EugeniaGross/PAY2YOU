from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets

from users.models import UserService

from .serializers import UserServiceListSerializer, UserServiceRetrieveSerializer, UserHistoryPaymentSerializer, UserServiceCreateSerialiser, UserServiceUpdateSerialiser
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
