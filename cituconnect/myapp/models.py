from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone

# Assuming you have a School model defined somewhere
class School(models.Model):
    name = models.CharField(max_length=255)
    # Add other fields as needed

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    member_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=[
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ])
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set_permissions')

class Post(models.Model):
    postId = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    content = models.TextField()
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='pending')
    priorityLevel = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    isAnonymous = models.BooleanField(default=False)
    member = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User
    approvedBy = models.CharField(max_length=30, null=True, blank=True)
    categoryId = models.ForeignKey('Category', on_delete=models.CASCADE)  # Assuming you have a Category model

class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)  # This will auto-increment
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    content = models.TextField()
    isRead = models.BooleanField(default=False)
    timeStamp = models.DateTimeField(default=timezone.now)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.content[:20]}"