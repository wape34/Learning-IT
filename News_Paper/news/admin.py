from django.contrib import admin
from news.models import Post, Author, Category, PostCategories, Comment


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategories)
admin.site.register(Comment)
