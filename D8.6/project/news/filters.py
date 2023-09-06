import django_filters
from django_filters import FilterSet
from .models import News, Author
from django import forms

class NewsFilter(FilterSet):
    name = django_filters.CharFilter(field_name='name',
                                            label="Поиск",
                                            lookup_expr='icontains',)
    author = django_filters.ModelChoiceFilter(field_name='author',
                                              label='Выбор автора',
                                              lookup_expr='exact',
                                              queryset=Author.objects.all())
    date = django_filters.DateFilter(field_name='time_create',
                                        widget=forms.DateInput(attrs={'type': 'date'}),
                                        label='Дата',
                                        lookup_expr='date__gte')

    class Meta:
        model = News
        fields = ['name', 'author', 'date']