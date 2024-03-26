from datetime import datetime

from django.db.models import Sum
from django.db.models import F

from users.models import UserTrialPeriod, UserSpecialCondition, UserService


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


def get_fut_expenses(obj, context):
    expense = UserService.objects.filter(
        user=context['request'].user,
        is_active=True,
        auto_pay=True
    ).aggregate(Sum('expense'))
    return expense['expense__sum']


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
