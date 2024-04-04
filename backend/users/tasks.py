from datetime import datetime

from django.conf import settings
from django.urls import reverse
from requests import post

from api_v1.exeptions import CashbackError, PaymentError
from api_v1.utils import connect_special_condition, create_subscribe, get_days
from backend.celery import app
from services.models import TariffSpecialCondition

from .models import UserService, UserTrialPeriod


def get_full_url(path):
    if settings.DEBUG:
        return f'http://127.0.0.1:8000/{path}'
    return f'{settings.SITE_URL}{path}'


@app.task
def cashback_accrual():
    month = datetime.now().month - 1
    year = datetime.now().year
    subscriptions = UserService.objects.filter(
        start_date__year=year,
        start_date__month=month
    )
    for subscription in subscriptions:
        url = get_full_url('cashback_accrual/')
        response = post(
            url,
            data={
                'user': subscription.user,
                'price': subscription.cashback
            }
        )
        if response.status_code != 200:
            raise CashbackError
        subscription.status_cashback = True
        subscription.save()


@app.task
def create_autopay():
    subscriptions = UserService.objects.filter(
        is_active=True,
        auto_pay=True
    )
    url = get_full_url('payment/')
    for subscription in subscriptions:
        if subscription.end_date < datetime.now().date():
            if UserTrialPeriod.objects.filter(
                user=subscription.user,
                service=subscription.service
            ).exists()\
                and UserTrialPeriod.objects.get(
                    user=subscription.user,
                    service=subscription.service
                ).end_date == subscription.end_date\
                and TariffSpecialCondition.objects.filter(
                    tariff=subscription.tariff
            ).exists():
                price = subscription.tariff.tariff_special_condition.price
                response = post(
                    url,
                    data={
                        'user': subscription.user,
                        'price': price
                    }
                )
                if response.status_code != 200:
                    raise PaymentError
                subscription.is_active = False
                subscription.save()
                days = get_days(subscription.tariff.tariff_special_condition)
                connect_special_condition(
                    object=subscription.tariff,
                    days=days,
                    user=subscription.user,
                    phone_number=subscription.phone_number
                )
            else:
                response = post(
                    url,
                    data={
                        'user': subscription.user,
                        'price': subscription.tariff.tariff_condition.price
                    }
                )
                if response.status_code != 200:
                    raise PaymentError
                subscription.is_active = False
                subscription.save()
                days = get_days(subscription.tariff.tariff_condition)
                create_subscribe(
                    object=subscription.tariff,
                    days=days,
                    user=subscription.user,
                    phone_number=subscription.phone_number
                )
    return url
