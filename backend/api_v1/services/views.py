from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from services.models import Service

from ..pagination import ServicePagination
from .serializers import (
    CustomTokenObtainPairSerializer,
    ServiceListSerializer,
    CategoryImageSerializer,
    ServiceCategoryImageSerializer,
    PopularServiceSerialiser,
    ServiceRetrieveSerializer,
    TariffListSerializer,
    TariffRetrieveSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ServiceParentViewSet(ListModelMixin, viewsets.GenericViewSet):
    pagination_class = ServicePagination


class SevicesViewSet(RetrieveModelMixin, ServiceParentViewSet):
    queryset = Service.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceRetrieveSerializer


class CategoryImageViewSet(ServiceParentViewSet):
    serializer_class = CategoryImageSerializer

    def get_queryset(self):
        service = get_object_or_404(
            Service,
            id=self.kwargs['service_id']
        )
        return service.category_images.all()


class ServiceCategoryImageViewSet(ServiceParentViewSet):
    serializer_class = ServiceCategoryImageSerializer

    def get_queryset(self):
        service = get_object_or_404(
            Service,
            id=self.kwargs['service_id']
        )
        category = get_object_or_404(
            service.category_images,
            id=self.kwargs['category_id']
        )
        return category.service_category_images.all()


class PopularServiceViewSet(ServiceParentViewSet):
    serializer_class = PopularServiceSerialiser

    def get_queryset(self):
        queryset = Service.objects.all(
        ).annotate(
            Count('user_services__is_active')
        ).order_by('-user_services__is_active__count')
        return queryset


class TariffViewSet(RetrieveModelMixin, ServiceParentViewSet):
    serializer_class = TariffListSerializer

    def get_queryset(self):
        service = get_object_or_404(
            Service,
            pk=self.kwargs['service_id']
        )
        return service.tariffs.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TariffListSerializer
        return TariffRetrieveSerializer
