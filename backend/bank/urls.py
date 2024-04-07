from django.urls import path

from .views import cashback_accrual, payment

app_name = 'bank'

urlpatterns = [
    path(
        'payment/',
        payment,
        name='payment'
    ),
    path(
        'cashback_accrual/',
        cashback_accrual,
        name='cashback_accrual'
    )
]
