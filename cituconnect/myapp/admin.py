from django.contrib import admin
from .models import User, Post, School, Category, Notification,Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('postId', 'content', 'status', 'member')
    list_filter = ('status',)
    search_fields = ('content', 'member__username')

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(School)
admin.site.register(Category)
admin.site.register(Notification)
admin.site.register(Comment)

