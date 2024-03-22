from django.contrib import admin

from .models import Service, CategoryImage, ServiceCategoryImage


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceCategoryImage)
class ServiceCategoryImageAdmin(admin.ModelAdmin):
    pass