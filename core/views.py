from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Comment
from .forms import CommentForm, PostForm, RegisterForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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

def forum(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)

            if request.user.is_authenticated:
                new_post.author = request.user
            else:
                anon_id = random.randint(10000000, 99999999)
                new_post.author_name = f"Anonymous#{anon_id}"

            new_post.save()
            return redirect('forum')
    else:
        post_form = PostForm()

    comment_form = CommentForm()

    return render(request, 'forum.html', {
        'posts': posts,
        'post_form': post_form,
        'comment_form': comment_form
    })

def like_post(request, post_id, action):
    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(Post, id=post_id)
    is_like = True if action == 'like' else False

    Like.objects.update_or_create(
        user=request.user,
        post=post,
        defaults={'is_like': is_like}
    )
    return redirect('forum')

def add_comment(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.post = post
            c.save()
    return redirect('forum')

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not request.user.is_authenticated:
        return redirect('login')

    if post.author != request.user:
        return HttpResponseForbidden("You're not allowed to delete this post.")

    post.delete()
    return redirect('forum')

def library(request): return render(request, 'library.html')
def draw(request): return render(request, 'draw.html')
def podcasts(request): return render(request, 'podcasts.html')
