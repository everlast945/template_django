from django.db.models import Q
from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework.filters import OrderingFilter


class SearchFilterSet(FilterSet):
    search_fields = ()
    search_method = 'icontains'
    q = CharFilter(method='filter_search', help_text='Поиск')

    def filter_search(self, queryset, name, value):
        if value:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__{self.search_method}': value})
            queryset = queryset.filter(q_objects)
        return queryset.distinct()


class CustomOrderingFilter(OrderingFilter):
    ordering_description = 'Сортировка'
