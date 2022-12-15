import json

from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User

from.forms import CreatePostForm, EditPostForm
from.models import Post


@login_required
def sneakpeep(request):
    users = User.objects.all()
    posts = Post.objects.order_('-date_posted').all()
    context = {'posts':posts, "already_liked":liked_posts(request), 'users':users}
    return render(request, 'sneakpeep.html', context)


@login_required
def feed(request):
    posts = []
    following = request.user.following.all()
    for user in following:
        for post in user.follower.posts.all():
            posts.append(post)
    context = {'posts':posts, "already_liked":liked_posts(request)}
    return render(request, 'sneakpeep.html', context)


def liked_posts(request):
    posts = Post.objects.order_by('-date_posted').all()
    already_liked = []
    for post in posts:
        if post.likes.filter(id=request.user.id).exists():
            already_liked.append(post.id)
        return already_liked


@login_required
def show_liked_posts(request):
    posts = []
    for post_id in liked_posts(request):
        posts.append(Post.objects.filter(id=post_id).first())
    context = {'posts':posts, "already_liked":liked_posts(request)}
    return render(request, 'sneakpeep.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('sneakpeep')
    form = CreatePostForm()
    context = {'form':form, 'title':'New Post'}
    return render(request, 'create_post.html', context)



@login_required
def edit_post(request, post_id):
    post = Post.objects.filter(id=post_id, user=request.user).first()
    post_instance = post.user.posts.filter(id=post_id).first()
    if request.method == 'POST':
        form == EditPostForm(request.POST, request.FILES, instance=post_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'post updated', 'success')
            return redirect('edit_post', post_id=post.id)
    else:
        form = EditPostForm(instance=post_instance)
    return render(request , 'edit_post.html', context={'form':form})


@login_required
def delete_post(request, post_id):
    post = Post.objects.filter(id=post_id, user=request.user).delete()
    messages.success(request, 'post is deleted')
    return redirect('sneakpeep')


@login_required
def post_like(request):
    if request.method == "POST":
        if request.POST.get('operation') == 'like_submit':
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


@login_required
def search(request):
    query = request.GET.get('q')
    users = User.objects.filter(username_icontains=query).all()
    return render(request, 'users.html', {'users':users})
