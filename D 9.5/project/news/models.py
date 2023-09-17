from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')
    def __str__(self):
        return self.name.title()
class News(models.Model):
    article = 'AR'
    news = "NW"

    POST = [(article, "статья"),
            (news, 'новость')]
    post = models.CharField(max_length=2, choices=POST, verbose_name='Вид поста', default='NW')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE,
        related_name='news',
    )
    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])

class NewsCategory(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()