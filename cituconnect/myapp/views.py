from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
            return render(request, 'all_posts.html', {'username': user.username, 'posts': user_posts})
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
    return render(request, 'registration/login.html')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.member = request.user
            post.save()
            return redirect('all_posts')
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
def my_posts_view(request):
    posts = Post.objects.filter(member=request.user)
    return render(request, 'hello_user.html', {'posts': posts})

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
        comment = Comment.objects.create(content=content, post=post, member=request.user)
        
        # Create a notification for the post owner if the commenter is not the post owner
        if post.member != request.user:
            notification_content = f"{request.user.username} commented on your post: {post.content[:20]}"
            Notification.objects.create(content=notification_content, recipient=post.member)
        
        return JsonResponse({'status': 'success'})

@csrf_exempt
@login_required
def update_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, comment_id=comment_id, member=request.user)
        new_content = request.POST.get('content')
        if new_content:
            comment.content = new_content
            comment.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id, member=request.user)
    if request.method == 'POST':
        comment.delete()
        #return redirect('hello_user')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
    #return render(request, 'delete_comment.html', {'comment': comment})

#@login_required
#def get_all_posts_by_registered_users():
#   # Assuming 'member' is a ForeignKey to the User model in the Post model
#    posts = Post.objects.filter(member__is_active=True)
#    return posts

@login_required
def all_posts_view(request):
    all_posts = Post.objects.all()
    return render(request, 'all_posts.html', {'posts': all_posts})
    #posts = Post.objects.filter(member__is_active=True)  # Fetch all posts by active users
    #print(len(posts))  # Debugging: Print the posts to the console
    #return render(request, 'all_posts.html', {'posts': posts})

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications.html', {'notifications': notifications})

@csrf_exempt
@login_required
def like_post_view(request, post_id):
    post = get_object_or_404(Post, postId=post_id)
    action = request.POST.get('action')
    liked = False
    disliked = False

    if action == 'like':
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
            disliked = False
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            liked = True
            if post.member != request.user:
                notification_content = f"{request.user.username} liked your post: {post.content[:20]}"
                Notification.objects.create(content=notification_content, recipient=post.member)
        else:
            post.likes.remove(request.user)
            liked = False
    elif action == 'dislike':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        if request.user not in post.dislikes.all():
            post.dislikes.add(request.user)
            disliked = True
            if post.member != request.user:
                notification_content = f"{request.user.username} disliked your post: {post.content[:20]}"
                Notification.objects.create(content=notification_content, recipient=post.member)
        else:
            post.dislikes.remove(request.user)
            disliked = False

    return JsonResponse({
        'liked': liked,
        'disliked': disliked,
        'likes_count': post.likes.count(),
        'dislikes_count': post.dislikes.count()
    })

#@csrf_exempt
#@login_required
#def dislike_post_view(request, post_id):
#    post = get_object_or_404(Post, postId=post_id)
#    disliked = False
#    if request.user in post.dislikes.all():
#        post.dislikes.remove(request.user)
#    else:
#        post.dislikes.add(request.user)
#        disliked = True
#    return JsonResponse({'disliked': disliked, 'dislikes_count': post.dislikes.count()})


@login_required
def comment_post_view(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = get_object_or_404(Post, postId=post_id)
        comment = Comment.objects.create(content=content, post=post, member=request.user)
        # Create a notification for the post owner if the commenter is not the owner
        if post.member != request.user:
            notification_content = f"{request.user.username} commented on your post: {post.content[:20]}"
            Notification.objects.create(content=notification_content, recipient=post.member)
        return JsonResponse({'status': 'success', 'comment_id': comment.comment_id})
    return JsonResponse({'status': 'error'})