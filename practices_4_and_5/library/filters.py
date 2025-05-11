import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Минимальная цена"
    )
    price_max = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Максимальная цена"
    )

    class Meta:
        model = Book
        fields = ["price_min", "price_max"]
