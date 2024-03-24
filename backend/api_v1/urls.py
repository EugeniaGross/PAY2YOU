from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .services.views import CustomTokenObtainPairView, SevicesViewSet, CategoryImageViewSet, ServiceCategoryImageViewSet, PopularServiceViewSet, TariffViewSet
from .users.views import UserServiceViewSet
router = SimpleRouter()

router.register(
    'services',
    SevicesViewSet,
    basename='services'
)
router.register(
    r'services/(?P<service_id>[a-z\d-]+)/image-categories',
    CategoryImageViewSet,
    basename='image-categories'
)
router.register(
    r'services/(?P<service_id>[a-z\d-]+)/image-categories/(?P<category_id>[a-z\d-]+)/images',
    ServiceCategoryImageViewSet,
    basename='images'
)
router.register(
    'popular-services',
    PopularServiceViewSet,
    basename='popular-services'
)
router.register(
    r'services/(?P<service_id>[a-z\d-]+)/tariffs',
    TariffViewSet,
    basename='tariffs'
)
router.register(
    'subscriptions',
    UserServiceViewSet,
    basename='subscriptions'
)


urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='create_jwt'),
    path('auth/', include('djoser.urls')),
    path('', include(router.urls))
]