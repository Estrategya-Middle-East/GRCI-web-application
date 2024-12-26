# filters.py
from django.db.models import F,Q
import django_filters
from .models import Risk

class RiskFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Risk
        fields = ['search']  # You can add other fields here as necessary

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(name__icontains=value) | Q(description__icontains=value)
            )
        return queryset  # If no search term, return the full queryset
