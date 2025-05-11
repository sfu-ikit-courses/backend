import django_filters
from .models import Article, Category


class ArticleFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search", label="Поиск")
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label="Категория",
        empty_label="Все категории",
    )

    class Meta:
        model = Article
        fields = ["q", "category"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(name__icontains=value) | queryset.filter(
            excerpt__icontains=value
        )
