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
        ).end_date > datetime.now().date()
    ):
        return obj.tariff.tariff_trial_period
    elif (
        UserSpecialCondition.objects.filter(
            user=obj.user,
            tariff=obj.tariff
        ).exists() and obj.tariff.special_conditions.get(
            user=user
        ).end_date > datetime.now().date()
    ):
        return obj.tariff.tariff_special_condition
    return obj.tariff.tariff_condition


def get_past_expenses(obj, context):
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
