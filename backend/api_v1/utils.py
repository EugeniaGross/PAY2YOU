from datetime import datetime

from users.models import UserTrialPeriod, UserSpecialCondition


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
    print(obj.tariff.special_conditions.get(
            user=user
        ).end_date)
    print(obj.service.trial_period.get(
            user=user
        ).end_date)
    return obj.tariff.tariff_condition


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
