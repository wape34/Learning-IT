from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .models import News, Category
from datetime import datetime
from .filters import NewsFilter
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
class NewsList(ListView):
    model = News
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'new.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_news',)
    form_class = NewsForm
    model = News
    template_name = 'new_edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.post = 'AR'
        post.save()
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_news')
    login_url = '/accounts/login/'
    form_class = NewsForm
    model = News
    template_name = 'new_edit.html'

class NewsDelete(DeleteView):
    model = News
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')

class ArticleUpdate(UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'article_edit.html'

class ArticleDelete(DeleteView):
    model = News
    template_name = 'article_delete.html'
    success_url = reverse_lazy('new_list')

class CategoryListView(ListView):
    model = News
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id = self.kwargs['pk'])
        queryset = News.objects.filter(category=self.category).order_by('-time_create')
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = "Вы успешно подписались на рассылку новостей категории"

    return render(request, 'subscribe.html', {'category': category, 'message': message})

