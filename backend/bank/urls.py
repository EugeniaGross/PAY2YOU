from django.urls import path

from .views import CashbackViewSet, PaymentViewSet

app_name = 'bank'

urlpatterns = [
    path('payment/', PaymentViewSet.as_view({'post': 'create'}), name='payment'),
    path('cashback_accrual/', CashbackViewSet.as_view({'post': 'create'}), name='cashback_accrual')
]
