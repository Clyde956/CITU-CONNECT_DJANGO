from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm, PostForm
from .models import Notification, Post, Comment

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_post')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_posts = Post.objects.filter(member=user)
            return render(request, 'hello_user.html', {'username': user.username, 'posts': user_posts})
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
    return render(request, 'registration/login.html')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.member = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user
            post.save()
            return redirect('success')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def success(request):
    return render(request, 'success.html')

@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, postId=post_id, member=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('hello_user')
    else:
        form = PostForm(instance=post)
    return render(request, 'update_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, postId=post_id, member=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('hello_user')
    return render(request, 'delete_post.html', {'post': post})

@login_required
def hello_user(request):
    posts = Post.objects.filter(member=request.user).prefetch_related('comments')
    return render(request, 'hello_user.html', {'posts': posts, 'username': request.user.username})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, postId=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
        content = f"{user.username} liked your post: {post.content[:20]}"
        Notification.objects.create(content=content, recipient=post.member)

    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})

@login_required
def notifications(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = get_object_or_404(Post, postId=post_id)
        Comment.objects.create(content=content, post=post, member=request.user)
        return JsonResponse({'status': 'success'})

@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id, member=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment.content = content
        comment.save()
        return redirect('hello_user')
    return render(request, 'update_comment.html', {'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id, member=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('hello_user')
    return render(request, 'delete_comment.html', {'comment': comment})