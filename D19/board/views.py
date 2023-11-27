from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Reply
from datetime import datetime
from .forms import PostForm, ReplyForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .permissions import IsOwnerOrReadOnly
from django.core.mail import send_mail


class PostList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'post.html'
    form_class = PostForm
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Reply.objects.filter(accepted=True, post_id=self.kwargs['pk']).order_by('time_create')
        context['comments'] = comments

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = self.object
            reply.user = self.request.user
            reply.send_notification_email()
            reply.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permissions_classes = (IsOwnerOrReadOnly)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        current_user = self.request.user
        self.object.user = current_user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    login_url = '/accounts/login/'
    model = Post
    template_name = 'post_edit.html'
    permissions_classes = (IsOwnerOrReadOnly)

    def get_object(self, queryset=None):
        obj = super(UpdateView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permissions_classes = (IsOwnerOrReadOnly)

    def get_object(self, queryset=None):
        obj = super(DeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


def pageNotFound(request, exception):
    return HttpResponseNotFound


class ReplyCreate(CreateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = Post.objects.get(pk=self.kwargs['pk'])
        current_user = self.request.user
        self.object.user = current_user
        send_mail(
            subject=f'Здравствуйте! На ваш пост {self.object.post.post_title} появился отклик от {self.object.user.username}.',
            message=self.object.reply_text,
            from_email='eduard_mir1996@mail.ru',
            recipient_list=[self.object.post.user.email]
        )
        return super().form_valid(form)


class ReplyUpdate(UpdateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_edit.html'


class ReplyDelete(DeleteView):
    model = Reply
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('post_list')


class ReplyDetail(DetailView):
    model = Reply
    template_name = 'reply.html'
    context_object_name = 'reply'


class ReplyList(ListView):
    model = Reply
    template_name = 'replies.html'
    ordering = '-time_create'
    context_object_name = 'replies'
    paginate_by = 3


@login_required
def user_posts(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user).order_by('-time_create')
    return render(request, 'user_posts.html', {'posts': posts})


@login_required
def user_replies(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user).order_by('-time_create')
    selected_post_id = request.GET.get('post')

    replies = Reply.objects.filter(post__user=current_user).order_by('-time_create')
    if selected_post_id:
        replies = replies.filter(post__id=selected_post_id)

    if request.method == 'GET':
        selected_post_id = request.GET.get('post')
        if selected_post_id:
            replies = replies.filter(post__id=selected_post_id)

    return render(request, 'user_replies.html',
                  {'posts': posts, 'replies': replies, 'selected_post_id': selected_post_id})


@login_required
def accept_reply(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.accepted = True
    reply.save()
    reply.send_accepted_email()
    return HttpResponseRedirect(reverse('user_replies'))
