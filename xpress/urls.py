from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('forum/', views.forum, name='forum'),
    path('like/<int:post_id>/<str:action>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('library/', views.library, name='library'),
    path('draw/', views.draw, name='draw'),
    path('podcasts/', views.podcasts, name='podcasts'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
