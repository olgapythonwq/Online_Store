from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .mixins import GroupRequiredMixin
from .models import Post
from .forms import PostForm

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-created_at')

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'  # Задаём имя переменной, под которым объект поста будет доступен в шаблоне.

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)  # Переопределяем метод, чтобы увеличивать количество просмотров.
        obj.views_count += 1
        obj.save(update_fields=['views_count'])  # Сохраняем объект, но только поле views_count.- Это оптимизированный способ, чтобы не обновлять все поля в базе, а только одно.
        return obj

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    group_required = 'ContentManager'
    success_url = reverse_lazy('blog:post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.owner != request.user and not request.user.groups.filter(name='ContentManager').exists():
            raise PermissionDenied("Вы не можете редактировать этот пост.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.owner != request.user and not request.user.groups.filter(name='ContentManager').exists():
            raise PermissionDenied("Вы не можете удалить этот пост.")
        return super().dispatch(request, *args, **kwargs)
