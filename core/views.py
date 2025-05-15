from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Comment
from .forms import CommentForm, PostForm, RegisterForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.models import User
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
    post_form = PostForm(request.POST or None)
    if request.method == 'POST' and post_form.is_valid():
        content = post_form.cleaned_data['content']
        new_post = post_form.save(commit=False)
        if request.user.is_authenticated:
            new_post.author = request.user
        else:
            new_post.author_name = f"Anonymous#{random.randint(10000000, 99999999)}"
        new_post.save()
        return redirect('forum')

    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'forum.html', {
        'page_obj': page_obj,
        'post_form': post_form,
        'comment_form': CommentForm()
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

    if not request.user.is_authenticated or post.author != request.user:
        return HttpResponseForbidden("You're not allowed to delete this post.")

    post.delete()
    return redirect('forum')

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        return HttpResponseForbidden("You're not allowed to delete this comment.")
    comment.delete()
    return redirect('forum')

def profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
        posts = Post.objects.filter(author=profile_user).order_by('-created_at')
        is_anon = False
    except User.DoesNotExist:
        posts = Post.objects.filter(author__isnull=True, author_name=username).order_by('-created_at')
        profile_user = None
        is_anon = True

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'anon_name': username if is_anon else None,
        'posts': posts
    })

def library(request): return render(request, 'library.html')
def draw(request): return render(request, 'draw.html')
def podcasts(request): return render(request, 'podcasts.html')
