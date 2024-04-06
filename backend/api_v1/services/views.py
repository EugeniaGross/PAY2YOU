from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from services.models import Service

from ..pagination import ServicePagination
from ..response_shema import (
    response_schema_dict_image_categories_list,
    response_schema_dict_popular_services_list,
    response_schema_dict_service_detail,
    response_schema_dict_service_image_categories_list,
    response_schema_dict_services_list, response_schema_dict_tariff_detail,
    response_schema_dict_tariffs_list)
from .serializers import (CategoryImageSerializer, PopularServiceSerialiser,
                          ServiceCategoryImageSerializer,
                          ServiceListSerializer, ServiceRetrieveSerializer,
                          TariffListSerializer, TariffRetrieveSerializer)


class ServiceParentViewSet(ListModelMixin, viewsets.GenericViewSet):
    pagination_class = ServicePagination


class SevicesViewSet(RetrieveModelMixin, ServiceParentViewSet):
    queryset = Service.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceRetrieveSerializer

    @swagger_auto_schema(
        operation_description=(
            'Список сервисов '
        ),
        responses=response_schema_dict_services_list
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Информация о сервисе '
        ),
        responses=response_schema_dict_service_detail
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CategoryImageViewSet(ServiceParentViewSet):
    serializer_class = CategoryImageSerializer

    def get_queryset(self):
        service = get_object_or_404(
            Service,
            id=self.kwargs['service_id']
        )
        return service.category_images.all()

    @swagger_auto_schema(
        operation_description=(
            'Список категорий постеров сервиса '
        ),
        responses=response_schema_dict_image_categories_list
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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

    @swagger_auto_schema(
        operation_description=(
            'Список изображений в категории '
        ),
        responses=response_schema_dict_service_image_categories_list
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PopularServiceViewSet(ServiceParentViewSet):
    serializer_class = PopularServiceSerialiser

    def get_queryset(self):
        queryset = Service.objects.all(
        ).annotate(
            Count('user_services__is_active')
        ).order_by('-user_services__is_active__count')
        return queryset

    @swagger_auto_schema(
        operation_description=(
            'Список сервисов в порядке убывания популярности '
        ),
        responses=response_schema_dict_popular_services_list
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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

    @swagger_auto_schema(
        operation_description=(
            'Список тарифов сервиса '
        ),
        responses=response_schema_dict_tariffs_list
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Подробная информация о тарифе сервиса. '
        ),
        responses=response_schema_dict_tariff_detail
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
