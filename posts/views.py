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
