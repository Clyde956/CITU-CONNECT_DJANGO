from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm, PostForm, UserProfileForm
from .models import Notification, Post, Comment
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from django.utils.timezone import localtime
from django.utils.dateformat import format


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Ensure request.FILES is included
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
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
            if user.is_staff:  # Check if the user is an admin
                return redirect('custom_admin_dashboard')  # Redirect admin users to the admin dashboard
            next_url = request.POST.get('next', 'all_posts')  # Default to 'all_posts' if 'next' is not provided
            return redirect(next_url)
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
    next_url = request.GET.get('next', 'all_posts')  # Default to 'all_posts' if 'next' is not provided
    return render(request, 'registration/login.html', {'next': next_url})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Ensure request.FILES is included
        if form.is_valid():
            post = form.save(commit=False)
            post.member = request.user
            post.save()
            return redirect('all_posts')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def landing_page(request):
    return render(request, 'landing_page.html')

def success(request):
    return render(request, 'success.html')

@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, postId=post_id, member=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Ensure request.FILES is included
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
    posts = Post.objects.filter(member=request.user).order_by('-timeStamp')
    return render(request, 'hello_user.html', {
        'user': request.user,
        'posts': posts,
        'is_admin': request.user.is_staff  # Add this line
    })


@login_required
def my_posts_view(request):
    posts = Post.objects.filter(member=request.user).order_by('-timeStamp')
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

#@login_required
#def notifications(request):
    #notifications = request.user.notifications.all().order_by('-timeStamp')
    #return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# cituconnect/myapp/views.py
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
        
        profile_picture_url = request.user.profile_picture.url if request.user.profile_picture else static('profile_pictures/default_profile.jpg')
        
        return JsonResponse({
            'status': 'success',
            'comment_id': comment.comment_id,
            'profile_picture_url': profile_picture_url,
            'username': request.user.username
        })

    return JsonResponse({'status': 'error'})

# cituconnect/myapp/views.py
from django.utils.timezone import localtime

@csrf_exempt
@login_required
def update_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, comment_id=comment_id, member=request.user)
        new_content = request.POST.get('content')
        if new_content:
            comment.content = new_content
            comment.save()
            timestamp = format(localtime(comment.timestamp), 'M. j, Y, g:i a')
            last_modified = format(localtime(comment.last_modified), 'M. j, Y, g:i a')
            return JsonResponse({
                'status': 'success',
                'timestamp': timestamp,
                'last_modified': last_modified
            })
    return JsonResponse({'status': 'error'})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id, member=request.user)
    if request.method == 'POST':
        comment.delete()
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
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')

    posts = Post.objects.filter(status='approved').order_by('-timeStamp')

    if category_filter:
        posts = posts.filter(categoryId__name=category_filter)

    if search_query:
        posts = posts.filter(Q(content__icontains=search_query) | Q(categoryId__name__icontains=search_query))

    # Calculate trending categories
    trending_categories = Post.objects.filter(status='approved').values('categoryId__name').annotate(
        num_posts=Count('postId'),
        num_comments=Count('comments'),
        unique_commenters=Count('comments__member', distinct=True)
    ).order_by('-num_posts', '-num_comments', '-unique_commenters')[:5]  # Get top 5 trending categories

    return render(request, 'all_posts.html', {
        'posts': posts,
        'trending_categories': trending_categories,
        'username': request.user.username,
        'is_admin': request.user.is_staff  # Add this line
    })

#@login_required
#def notifications_view(request):
    #notifications = Notification.objects.filter(recipient=request.user)
    #return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def notifications_view(request):
    today = timezone.now().date()
    notifications = request.user.notifications.all().order_by('-timeStamp')
    unread_recent_notifications = notifications.filter(isRead=False, timeStamp__date=today)
    read_recent_notifications = notifications.filter(isRead=True, timeStamp__date=today)
    older_notifications = notifications.exclude(timeStamp__date=today)

    # Track displayed notifications in session
    displayed_notifications = request.session.get('displayed_notifications', [])
    new_displayed_notifications = list(unread_recent_notifications.values_list('notification_id', flat=True))
    request.session['displayed_notifications'] = displayed_notifications + new_displayed_notifications

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        unread_count = request.user.notifications.filter(isRead=False).count()
        return JsonResponse({'unread_count': unread_count})

    return render(request, 'notifications.html', {
        'unread_recent_notifications': unread_recent_notifications,
        'read_recent_notifications': read_recent_notifications,
        'older_notifications': older_notifications,
        'is_admin': request.user.is_staff  # Add this line
    })

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

# cituconnect/myapp/views.py
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm

@login_required
def profile_settings(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)  # Re-authenticate the user
            return redirect('hello_user')  # Redirect to a page that shows the updated profile
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'profile_settings.html', {
        'form': form,
        'user': request.user,
        'is_admin': request.user.is_staff  # Add this line
    })