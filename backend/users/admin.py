from django.contrib import admin

from .models import UserService, UserSpecialCondition, UserTrialPeriod


@admin.register(UserService)
class UserServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(UserTrialPeriod)
class UserTrialPeriodAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSpecialCondition)
class UserSpecialConditionAdmin(admin.ModelAdmin):
    pass
