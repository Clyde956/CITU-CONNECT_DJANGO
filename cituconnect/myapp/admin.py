from django.contrib import admin
from .models import User, Post, School, Category, Notification

admin.site.register(User)
admin.site.register(Post)
admin.site.register(School)
admin.site.register(Category)
admin.site.register(Notification)
