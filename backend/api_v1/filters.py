from django_filters import rest_framework as filter

from users.models import UserService


class UserServiceFilter(filter.FilterSet):
    is_active = filter.NumberFilter(
        method='filter_is_active'
    )

    class Meta:
        model = UserService
        fields = (
            'is_active',
        )

    def filter_is_active(self, queryset, name, value):
        if value == 0:
            return queryset.filter(auto_pay=False, is_active=False)
        if value == 1:
            return queryset.filter(is_active=True)
        return queryset


class UserServiceDateFilter(filter.FilterSet):
    start_date = filter.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = filter.DateFilter(field_name='start_date', lookup_expr='lte')

    class Meta:
        model = UserService
        fields = (
            'start_date',
            'end_date'
        )
