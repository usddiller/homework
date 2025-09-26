from typing import Any

from loguru import logger
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import BaseFilterBackend
from django.db.models import Q, QuerySet


class SearchFilter(BaseFilterBackend):
    def filter_queryset(
        self, 
        request: Request, 
        queryset: QuerySet, 
        view: ModelViewSet | Any
    ):
        search_fields: list = getattr(view, "search_fields", [])
        search_value = request.query_params.get("search")
        if not search_value:
            logger.info("There is no search value")
            return queryset
        logger.info("We get value, let's filter this shit")
        query = Q()
        for field in search_fields:
            query |= Q(**{f"{field}__icontains": search_value})
            
        return queryset.filter(query)
        

class SortFilter(BaseFilterBackend):
    """
    Создайте фильтр сортировки по date_joined
    Во вьюшке создайте атрибут sort_by_fields
    """