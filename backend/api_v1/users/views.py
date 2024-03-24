from rest_framework import viewsets

from users.models import UserService

from .serializers import UserServiceListSerializer, UserServiceRetrieveSerializer
from ..pagination import ServicePagination


class UserServiceViewSet(viewsets.ModelViewSet):
    pagination_class = ServicePagination

    def get_queryset(self):
        return UserService.objects.filter(
            user=self.request.user
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return UserServiceListSerializer
        return UserServiceRetrieveSerializer
