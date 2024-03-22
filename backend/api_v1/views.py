from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from services.models import Service

from .pagination import ServicePagination
from .serializers import CustomTokenObtainPairSerializer, ServiceSerializer, CategoryImageSerializer, ServiceCategoryImageSerializer, PopularServiceSerialiser


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer


class ServiceParentViewSet(ListModelMixin, viewsets.GenericViewSet):
    pagination_class = ServicePagination


class SevicesViewSet(RetrieveModelMixin, ServiceParentViewSet):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.only(
            'id',
            'image_logo',
            'name',
            'cashback'
        ).exclude(
            user_services__user=self.request.user,
            user_services__is_active=1
        )


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


class PopularServiceViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PopularServiceSerialiser
    pagination_class = ServicePagination

    def get_queryset(self):
        queryset = Service.objects.all(
        ).annotate(
            Count('user_services__is_active')
        ).order_by('-user_services__is_active__count')
        return queryset