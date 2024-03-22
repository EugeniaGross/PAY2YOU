from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CustomTokenObtainPairView, SevicesViewSet, CategoryImageViewSet, ServiceCategoryImageViewSet, PopularServiceViewSet

router = SimpleRouter()

router.register(
    'services',
    SevicesViewSet,
    basename='services'
)
router.register(
    r'services/(?P<service_id>[a-z\d-]+)/posterCategories',
    CategoryImageViewSet,
    basename='posterCategories'
)
router.register(
    r'services/(?P<service_id>[a-z\d-]+)/posterCategories/(?P<category_id>[a-z\d-]+)/gallery',
    ServiceCategoryImageViewSet,
    basename='gallery'
)
router.register(
    'recommendedServices',
    PopularServiceViewSet,
    basename='recommendedServices'
)

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='create_jwt'),
    path('auth/', include('djoser.urls')),
    path('', include(router.urls))
]