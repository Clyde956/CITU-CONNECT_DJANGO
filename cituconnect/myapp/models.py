from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class School(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    contact_info = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    member_id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=[
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('faculty', 'Faculty'),
    ])
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set_permissions')

class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Post(models.Model):
    postId = models.AutoField(primary_key=True)
    content = models.TextField()
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='pending')
    priorityLevel = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    isAnonymous = models.BooleanField(default=False)
    approvedBy = models.CharField(max_length=30, null=True, blank=True)
    categoryId = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_post = Post.objects.get(pk=self.pk)
            if old_post.status != self.status:
                self.create_status_change_notification()
        super().save(*args, **kwargs)

    def create_status_change_notification(self):
        content = f"Your post '{self.content[:20]}...' has been {self.status}. Check it out!"
        Notification.objects.create(content=content, recipient=self.member)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    content = models.TextField()
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

# cituconnect/myapp/models.py
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    content = models.TextField()
    isRead = models.BooleanField(default=False)
    timeStamp = models.DateTimeField(default=timezone.now)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.content[:20]}"