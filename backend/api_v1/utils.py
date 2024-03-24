from datetime import datetime

from users.models import UserTrialPeriod, UserSpecialCondition


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
            service=obj.service
        ).exists() and obj.tariff.special_conditions.get(
            user=user
        ).end_date > datetime.now().date()
    ):
        return obj.tariff.tariff_special_condition
    return obj.tariff.tariff_condition
