from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('forum/', views.forum, name='forum'),
    path('like/<int:post_id>/<str:action>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('library/', views.library, name='library'),
    path('draw/', views.draw, name='draw'),
    path('podcasts/', views.podcasts, name='podcasts'),
    path('profile/', views.profile)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)