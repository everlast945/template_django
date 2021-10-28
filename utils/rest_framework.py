from collections import OrderedDict

from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_description = 'Номер страницы'
    page_size_query_description = 'Количество записей'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('results', data),
            ('page_count', self.page.paginator.num_pages),
        ]))


def custom_exception_handler(exc, context):
    """
    Вывод ошибков с кодами исключений
    """
    if isinstance(exc, APIException):
        exc.detail = exc.get_full_details()
    return exception_handler(exc, context)
