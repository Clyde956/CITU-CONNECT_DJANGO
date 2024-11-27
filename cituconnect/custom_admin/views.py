from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myapp.models import Post  # Import the Post model

@login_required
def dashboard(request):
    posts = Post.objects.all().order_by('-timeStamp')
    return render(request, 'custom_admin/dashboard.html', {'posts': posts, 'username': request.user.username})