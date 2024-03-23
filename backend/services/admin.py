from django.contrib import admin

from .models import Service, CategoryImage, ServiceCategoryImage, CategoryService, Tariff, TariffSpecialCondition, TariffCondition


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceCategoryImage)
class ServiceCategoryImageAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryService)
class CategoryServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    pass


@admin.register(TariffSpecialCondition)
class TariffSpecialCondition(admin.ModelAdmin):
    pass


@admin.register(TariffCondition)
class TariffCondition(admin.ModelAdmin):
    pass