from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Post, Category, Author, Comment
from .filters import PostFilter
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import Group, User


# @login_required
# def add_comment(request, post_id, ):
#     user = request.user
#     post = Post.objects.get(id=post_id)
#     text=


@login_required
def subscribe_category(request, category_id, post_id):
    user = request.user
    category = Category.objects.get(id=category_id)
    category.subcribes.add(user)
    # message = "You have successfully subscribed"
    return redirect(f"/posts/{post_id}")


@login_required
def subscribe_author(request, author_id, post_id):
    user = request.user
    author = Author.objects.get(id=author_id)
    author.subcribes.add(user)
    # message="You have successfully subscribed"
    return redirect(f"/posts/{post_id}")


class GroupMixin(UserPassesTestMixin):
    def check_group(self):
        return self.request.user.groups.filter(name='author').exists()

    def test_func(self):
        # Вызываем ваш метод check_group() для проверки наличия пользователя в группе 'author'
        return self.check_group()

    login_url = '/'


class PostsList(ListView):
    model = Post
    ordering = "heading"
    template_name = "posts.html"
    context_object_name = "posts"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_author'] = self.request.user.groups.filter(name='author').exists()
        return context


class PostDetails(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"

    # form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author_post'] = self.request.user == self.object.author.user_id
        context['is_comments'] = not Comment.objects.filter(post_id=self.object.id).all() == 0
        context['comments'] = Comment.objects.filter(post_id=self.object.id).all()
        # context['comment_form'] = CommentForm(initial={'post': self.object})
        return context

    # @login_required
    # def form_valid(self, form):
    #     form.instance.post = self.object
    #     form.instance.user_id = self.request.user
    #     return super().form_valid(form)


class PostCreate(GroupMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user_id=self.request.user)

        post = form.save(commit=False)
        post.author = author  # Присваиваем созданного или существующего автора
        if self.request.path == "/posts/news/create":
            post.state = 'NE'
        post.save()
        return super().form_valid(form)


class PostUpdate(GroupMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(GroupMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CommentCreate(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = "add_comment.html"

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        comment = form.save(commit=False)
        comment.user_id = self.request.user # Присваиваем созданного или существующего автора
        comment.post_id = post_id
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(id=self.kwargs['post_id'])
        context['is_comments'] = not Comment.objects.filter(post_id=self.kwargs['post_id']).all() == 0
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['post_id']).all()

        return context

    def get_success_url(self):
        return f"http://127.0.0.1:8000/posts/{self.kwargs["post_id"]}"