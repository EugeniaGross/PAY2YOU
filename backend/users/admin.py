from django.contrib import admin

from .models import UserService


@admin.register(UserService)
class UserServiceAdmin(admin.ModelAdmin):
    pass
