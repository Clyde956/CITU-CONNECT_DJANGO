from django.urls import path, include
from .views import (
    register, login_view, create_post, landing_page, success, update_post, delete_post,
    hello_user, my_posts_view, like_post, logout_view, add_comment,
    update_comment, delete_comment, all_posts_view, like_post_view, comment_post_view, notifications_view, profile_settings
)

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('create_post/', create_post, name='create_post'),
    path('success/', success, name='success'),
    path('update_post/<int:post_id>/', update_post, name='update_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('hello_user/', hello_user, name='hello_user'),
    path('my_posts/', my_posts_view, name='my_posts'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('notifications/', notifications_view, name='notifications'),
    path('logout/', logout_view, name='logout'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('update_comment/<int:comment_id>/', update_comment, name='update_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('all_posts/', all_posts_view, name='all_posts'),
    path('like_post_view/<int:post_id>/', like_post_view, name='like_post_view'),
    path('comment_post/<int:post_id>/', comment_post_view, name='comment_post'),
    path('profile_settings/', profile_settings, name='profile_settings'),
    path('custom-admin/', include('custom_admin.urls')),  # Include custom admin URLs
]