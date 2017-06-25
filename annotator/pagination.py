from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class SearchPagination(PageNumberPagination):

    page_query_param = 'offset'
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'rows': data
        })
