from django.contrib import admin
from .models import Category, News, Author


class NewsAdmin(admin.ModelAdmin):

    list_display = ('name', 'description', 'category')
    list_filter = ('name', 'description', 'category')
    search_fields = ('name', 'category__name')

admin.site.register(Category)
admin.site.register(News, NewsAdmin)
admin.site.register(Author)
