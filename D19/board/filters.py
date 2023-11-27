import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):
    post_title = django_filters.CharFilter(lookup_expr='icontains', label='Title')

    class Meta:
        model = Post
        fields = ['post_title']
