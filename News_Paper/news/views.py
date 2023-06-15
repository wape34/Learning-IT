from django.shortcuts import render
from django.views.generic import ListView, DetailView
from news.models import Post


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-datetime_in'


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    pk_url_kwarg = 'id'
