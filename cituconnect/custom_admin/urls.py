from django.urls import path
from .views import dashboard, update_post_status
from . import views

urlpatterns = [
    path('', views.dashboard, name='custom_admin_dashboard'),
    path('update_post_status/<int:post_id>/', update_post_status, name='update_post_status'),
]