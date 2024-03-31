from backend.celery import app
from .models import UserService, UserTrialPeriod, UserSpecialCondition
from services.models import TariffSpecialCondition
from datetime import datetime, timedelta
from api_v1.utils import get_days
from math import floor


@app.task
def cashback_accrual():
    month = datetime.now().month - 1
    year = datetime.now().year
    subscriptions = UserService.objects.filter(
        start_date__year=year,
        start_date__month=month
    )
    for subscription in subscriptions:
        subscription.status_cashback = True
        subscription.save()


@app.task
def create_autopay():
    subscriptions = UserService.objects.filter(
        is_active=True,
        auto_pay=True
    )
    for subscription in subscriptions:
        if subscription.end_date < datetime.now().date():
            if (UserTrialPeriod.objects.filter(
                    user=subscription.user,
                    service=subscription.service
                ).exists()
                and UserTrialPeriod.objects.get(
                    user=subscription.user,
                    service=subscription.service
                ).end_date == subscription.end_date
                and TariffSpecialCondition.objects.filter(
                    tariff=subscription.tariff
                ).exists()
            ):
                subscription.is_active=False
                subscription.save()
                days = get_days(subscription.tariff.tariff_special_condition)
                UserService.objects.create(
                    user=subscription.user,
                    service=subscription.service,
                    tariff=subscription.tariff,
                    start_date=datetime.now().date(),
                    end_date=datetime.now().date() + timedelta(days=days),
                    expense=subscription.tariff.tariff_special_condition.price,
                    cashback=0,
                    is_active=True,
                    auto_pay=True,
                    status_cashback=False,
                    phone_number=subscription.phone_number
                )
                UserSpecialCondition.objects.create(
                    user=subscription.user,
                    tariff=subscription.tariff,
                    start_date=datetime.now().date(),
                    end_date=datetime.now().date() + timedelta(days=days)
                )
            else:
                subscription.is_active=False
                subscription.save()
                days = get_days(subscription.tariff.tariff_condition)
                price = subscription.tariff.tariff_condition.price
                cashback = subscription.tariff.service.cashback
                UserService.objects.create(
                    user=subscription.user,
                    service=subscription.tariff.service,
                    tariff=subscription.tariff,
                    start_date=datetime.now().date(),
                    end_date=datetime.now().date() + timedelta(days=days),
                    expense=subscription.tariff.tariff_condition.price,
                    cashback=floor(price * cashback / 100),
                    is_active=True,
                    auto_pay=True,
                    status_cashback=False,
                    phone_number=subscription.phone_number
                )
