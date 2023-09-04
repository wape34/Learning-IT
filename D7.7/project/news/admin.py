from django.contrib import admin
from .models import Category, News, Author


admin.site.register(Category)
admin.site.register(News)
admin.site.register(Author)
