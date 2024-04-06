from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from .services.views import (CategoryImageViewSet, PopularServiceViewSet,
                             ServiceCategoryImageViewSet, SevicesViewSet,
                             TariffViewSet)
from .users.views import (CashbackViewSet, CustomTokenObtainPairView,
                          CustomUserViewSet, ExpensesByCategoryViewSet,
                          ExpensesViewSet, FutureExpensesViewSet,
                          UserHistoryPaymentViewSet, UserServiceViewSet)

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
    r'services/(?P<service_id>[a-z\d-]+)'
    r'/image-categories/(?P<category_id>[a-z\d-]+)/images',
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
router.register(
    'payment-history',
    UserHistoryPaymentViewSet,
    basename='payment-history'
)
router.register(
    'analytics/expenses',
    ExpensesViewSet,
    basename='expenses'
)
router.register(
    'analytics/expenses-by-category',
    ExpensesByCategoryViewSet,
    basename='expenses-by-category'
)
router.register(
    'analytics/future-expenses',
    FutureExpensesViewSet,
    basename='future-expenses'
)
router.register(
    'analytics/cashback',
    CashbackViewSet,
    basename='cashback'
)

urlpatterns = [
    path(
        'login/',
        CustomTokenObtainPairView.as_view(),
        name='create_jwt'
    ),
    path(
        'registration/',
        CustomUserViewSet.as_view({'post': 'create'}),
        name='users'
    ),
    path(
        '',
        include(router.urls)
    )
]

schema_view = get_schema_view(
   openapi.Info(
      title="PAY2YOU API",
      default_version='v1',
      description="Документация для мобильного приложения PAY2YOU",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$',
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/', schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'),
   url(r'^redoc/', schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'),
]
