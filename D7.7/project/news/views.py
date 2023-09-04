from .models import News
from datetime import datetime
from .filters import NewsFilter
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import NewsForm
from django.urls import reverse_lazy
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

class NewsCreate(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'new_edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.post = 'AR'
        post.save()
        return super().form_valid(form)

class NewsUpdate(UpdateView):
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
