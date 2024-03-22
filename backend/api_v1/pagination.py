from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class ServicePagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'skip'
    offset_query_param = 'top'
    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'previousLink': self.get_previous_link(),
            'nextLink': self.get_next_link()
        })