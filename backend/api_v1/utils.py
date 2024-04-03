from datetime import datetime, timedelta
from math import floor

from django.db.models import F, Sum

from users.models import UserService, UserSpecialCondition, UserTrialPeriod


def get_tariff_condition(obj, user):
    if (
        UserTrialPeriod.objects.filter(
            user=obj.user,
            service=obj.service
        ).exists() and obj.service.trial_period.get(
            user=user
        ).end_date == obj.end_date
    ):
        return obj.tariff.tariff_trial_period
    elif (
        UserSpecialCondition.objects.filter(
            user=obj.user,
            tariff=obj.tariff
        ).exists() and obj.tariff.special_conditions.get(
            user=user
        ).end_date == obj.end_date
    ):
        return obj.tariff.tariff_special_condition
    return obj.tariff.tariff_condition


def get_past_expenses_category(obj, context):
    start_date = datetime.strptime(
        context.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(context.get('end_date'), '%Y-%m-%d')
    expense = UserService.objects.filter(
        user=context['request'].user,
        start_date__range=(start_date, end_date)
    ).values(
        'service__category__name'
    ).annotate(
        name=F('service__category__name'), expenses=Sum('expense')
    )
    return expense


def get_days(tariff_condition):
    if tariff_condition.period == 'M':
        return tariff_condition.count * 30
    elif tariff_condition.period == 'Y':
        return tariff_condition.count * 30 * 12
    else:
        return tariff_condition.count


def get_full_name_period(count, period):
    if count % 10 == 1 and count % 100 != 11:
        if period == 'D':
            return 'День'
        if period == 'M':
            return 'Месяц'
        if period == 'Y':
            return 'Год'
    elif count % 10 in (2, 3, 4) and count % 100 not in (12, 13, 14):
        if period == 'D':
            return 'Дня'
        if period == 'M':
            return 'Месяца'
        if period == 'Y':
            return 'Года'
    else:
        if period == 'D':
            return 'Дней'
        if period == 'M':
            return 'Месяцев'
        if period == 'Y':
            return 'Лет'


def connect_special_condition(object, days, user=None, phone_number=None):
    user_service = UserService.objects.create(
        user=user,
        service=object.service,
        tariff=object,
        start_date=datetime.now().date(),
        end_date=datetime.now().date() + timedelta(days=days),
        expense=object.tariff_special_condition.price,
        cashback=0,
        is_active=True,
        auto_pay=True,
        status_cashback=False,
        phone_number=phone_number
    )
    UserSpecialCondition.objects.create(
        user=user,
        tariff=object,
        start_date=datetime.now().date(),
        end_date=datetime.now().date() + timedelta(days=days)
    )
    return user_service


def create_subscribe(object, days, user, phone_number):
    price = object.tariff_condition.price
    cashback = object.service.cashback
    subscribe = UserService.objects.create(
        user=user,
        service=object.service,
        tariff=object,
        start_date=datetime.now().date(),
        end_date=datetime.now().date() + timedelta(days=days),
        expense=object.tariff_condition.price,
        cashback=floor(price * cashback / 100),
        is_active=True,
        auto_pay=True,
        status_cashback=False,
        phone_number=phone_number
    )
    return subscribe
