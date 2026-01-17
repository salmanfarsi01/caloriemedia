from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as user_views
from feed import views as feed_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', feed_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
    # NEW URLS
    path('like/<int:pk>/', feed_views.like_post, name='like-post'),
    path('post/<int:pk>/delete/', feed_views.delete_post, name='post-delete'),
    path('post/<int:pk>/update/', feed_views.update_post, name='post-update'),
    path('api/chat/', feed_views.chat_api, name='chat-api'),
    # Add this line inside urlpatterns
    path('post/<int:pk>/repost/', feed_views.repost_post, name='post-repost'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)