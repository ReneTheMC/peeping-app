from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import HttpResponse

from .forms import CreatePostForm, EditPostForm
from .models import Post


@login_required
def home(request):
    posts = Post.objects.order_by('-date_posted').all()
    already_liked = []
    for post in posts:
       if post.likes.filter(id=request.user.id).exists():
           already_liked.append(post.id)
    return render(request, 'home.html', context={'posts':posts,"already_liked":already_liked})


@login_required 
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('home')
    form = CreatePostForm()
    context = {'form':form, 'title':'New Post'}
    return render(request, 'create_post.html', context) 


@login_required
def edit_post(request, post_id):
    post = Post.objects.filter(id=post_id, user=request.user).first()
    post_instance = post.user.posts.filter(id=post_id).first()
    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'your post updated successfully', 'success')
            return redirect('edit_post', post_id=post.id)
    else:
        form = EditPostForm(instance=post_instance)
    return render(request ,'edit_post.html', context={'form':form})


@login_required
def delete_post(request, post_id):
    post = Post.objects.filter(id=post_id, user=request.user).delete()
    messages.success(request, 'your post deleted successfully', 'danger')
    return redirect('home')


@login_required
def post_like(request):
    if request.method == "POST":
        if request.POST.get("operation") == "like_submit":
            content_id = request.POST.get("content_id", None)
            content = get_object_or_404(Post, id=content_id)
            if content.likes.filter(id=request.user.id):
                content.likes.remove(request.user)
                liked = False
            else:
                content.likes.add(request.user) 
                liked = True
    ctx = {"likes_count":content.total_likes, "liked":liked, "content_id":content_id}
    return HttpResponse(json.dumps(ctx), content_type='application/json')