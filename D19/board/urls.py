from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, ReplyCreate, ReplyUpdate, ReplyDelete, ReplyList, ReplyDetail, user_posts, user_replies, accept_reply, pageNotFound


handler404 = pageNotFound

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/reply_create/', ReplyCreate.as_view(), name='reply_create'),
    path('reply/<int:pk>/update/', ReplyUpdate.as_view(), name='reply_update'),
    path('reply/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),
    path('replies/', ReplyList.as_view(), name='reply_list'),
    path('reply/<int:pk>/', ReplyDetail.as_view(), name='reply_detail'),
    path('user_posts/', user_posts, name='user_posts'),
    path('user_replies/', user_replies, name='user_replies'),
    path('accept_reply/<int:pk>/', accept_reply, name='accept_reply')
]
