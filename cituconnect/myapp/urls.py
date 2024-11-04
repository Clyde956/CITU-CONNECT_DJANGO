from django.urls import path
from .views import register, login_view, create_post, home, success, update_post, delete_post, hello_user, notifications, like_post, logout_view, add_comment, update_comment, delete_comment

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('create_post/', create_post, name='create_post'),
    path('success/', success, name='success'),
    path('update_post/<int:post_id>/', update_post, name='update_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('hello_user/', hello_user, name='hello_user'),
    path('notifications/', notifications, name='notifications'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('logout/', logout_view, name='logout'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('update_comment/<int:comment_id>/', update_comment, name='update_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
]