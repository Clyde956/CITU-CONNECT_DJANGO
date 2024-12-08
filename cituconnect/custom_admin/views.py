from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from myapp.models import Post  # Import the Post model

@login_required
def dashboard(request):
    posts = Post.objects.all().order_by('-timeStamp')
    return render(request, 'custom_admin/dashboard.html', {
        'posts': posts,
        'username': request.user.username,
        'is_admin': True  # Pass a context variable indicating the user is an admin
    })

@csrf_exempt
@login_required
def update_post_status(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, postId=post_id)
        data = json.loads(request.body)
        status = data.get('status')
        if status in ['approved', 'rejected']:
            post.status = status
            post.approvedBy = request.user.username  # Set the approvedBy attribute to the admin's username
            post.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid status'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

