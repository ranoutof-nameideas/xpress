# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Comment
from .forms import CommentForm, RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

def forum(request):
    posts = Post.objects.all()
    return render(request, 'forum.html', {'posts': posts})

def like_post(request, post_id, action):
    post = get_object_or_404(Post, id=post_id)
    is_like = action == 'like'
    Like.objects.update_or_create(user=request.user, post=post, defaults={'is_like': is_like})
    return redirect('forum')

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.post = post
            c.save()
    return redirect('forum')

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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def podcasts(request):
    return render(request, 'podcasts.html')

def library(request):
    return render(request, 'library.html')

def draw(request):
    return render(request, 'draw.html')
