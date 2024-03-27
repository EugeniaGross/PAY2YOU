from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

from services.models import Service

from ..pagination import ServicePagination
from .serializers import (
    ServiceListSerializer,
    CategoryImageSerializer,
    ServiceCategoryImageSerializer,
    PopularServiceSerialiser,
    ServiceRetrieveSerializer,
    TariffListSerializer,
    TariffRetrieveSerializer,
)


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
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                'cashback': openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                )
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
            'Информация о сервисе '
        )
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
        responses={
            status.HTTP_200_OK: openapi.Schema(
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
                                'name': openapi.Schema(
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
                                'title': openapi.Schema(
                                 type=openapi.TYPE_STRING
                                ),
                                'image': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                )
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
                                'cashback': openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                )
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
                                'name': openapi.Schema(
                                 type=openapi.TYPE_STRING
                                ),
                                'descrition': openapi.Schema(
                                    type=openapi.TYPE_STRING
                                )
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
            'Подробная информация о тарифе сервиса '
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    'decsription': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    'condition': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'count': openapi.Schema(
                                type=openapi.TYPE_INTEGER
                            ),
                            'period': openapi.Schema(
                                type=openapi.TYPE_STRING
                            ),
                            'price': openapi.Schema(
                                type=openapi.TYPE_INTEGER
                            )
                        }
                    ),
                    'special_condition': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'count': openapi.Schema(
                                type=openapi.TYPE_INTEGER
                            ),
                            'period': openapi.Schema(
                                type=openapi.TYPE_STRING
                            ),
                            'price': openapi.Schema(
                                type=openapi.TYPE_INTEGER
                            )
                        }
                    ),
                    'trial_period': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'count': openapi.Schema(
                                type=openapi.TYPE_INTEGER
                            ),
                            'period': openapi.Schema(
                                type=openapi.TYPE_STRING
                            ),
                            'price': openapi.Schema(
                                type=openapi.TYPE_INTEGER
                            )
                        }
                    ),
                }
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
