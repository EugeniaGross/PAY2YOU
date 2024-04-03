from django.urls import path

from .views import create_payment, get_cashback

urlpatterns = [
    path('payment/', create_payment, name='payment'),
    path('cashback_accrual', get_cashback, name='cashback_accrual')
]
