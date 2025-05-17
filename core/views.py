from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Comment
from .forms import CommentForm, PostForm, RegisterForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import random

def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def like_post(request, post_id, action):
    post = get_object_or_404(Post, id=post_id)
    is_like = True if action == 'like' else False
    Like.objects.update_or_create(user=request.user, post=post, defaults={'is_like': is_like})
    return redirect('forum')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('forum')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('forum')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('forum')

from django.core.paginator import Paginator

def forum(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            if request.user.is_authenticated:
                new_post.author = request.user
            else:
                new_post.author_name = f"Anonymous#{random.randint(10000000, 99999999)}"
            new_post.save()
            return redirect('forum')
    else:
        post_form = PostForm()

    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    comment_form = CommentForm()

    return render(request, 'forum.html', {
        'page_obj': page_obj,
        'post_form': post_form,
        'comment_form': comment_form,
    })


def library(request): return render(request, 'library.html')
def draw(request): return render(request, 'draw.html')
def podcasts(request): return render(request, 'podcasts.html')
def profile(request): return render(request, 'profile.html')
