from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, ArticleUpdate, ArticleDelete, CategoryListView, subscribe



urlpatterns = [
   path('', NewsList.as_view(), name='new_list'),
   path('<int:pk>', NewsDetail.as_view(),name='new_detail'),
   path('create/', NewsCreate.as_view(), name='news.urls'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='new_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='new_delete'),
   path('articles/create/', NewsCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe')

]

