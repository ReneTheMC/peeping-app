from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreatePostForm
from .models import Post, Vote


@login_required
def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', context={'posts':posts})


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
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Vote(post=post, user=request.user)
    like.save()
    messages.success(request, 'you liked successfully', 'success')
    return redirect('home')


@login_required
def post_dislike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like = Vote.objects.filter(post=post, user=request.user)
    like.delete()
    messages.success(request, 'you disliked successfully', 'warning')
    return redirect('home')