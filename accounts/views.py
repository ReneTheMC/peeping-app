from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UserRegisterForm, EditAvatarForm, EditInformationForm
from posts.models import Post


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                'Your account has been created! You are now able to log in'
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request, username):
    users = User.objects.all()
    user = User.objects.filter(username=username).first()
    posts = Post.objects.filter(user=user).all()
    already_liked = []
    for post in posts:
       if post.likes.filter(id=request.user.id).exists():
           already_liked.append(post.id)
    return render(request, 'profile.html', context={'user':user, 'posts':posts, 'already_liked':already_liked, 'users':users})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        avatar_form = EditAvatarForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        information_form = EditInformationForm(
            request.POST, instance=request.user
        )
        if avatar_form.is_valid() and information_form.is_valid():
            avatar_form.save()
            information_form.save()
            return redirect('profile', username=request.user.username)
    else:
        avatar_form = EditAvatarForm(instance=request.user.profile)
        information_form = EditInformationForm(instance=request.user)
    
    context = {
        'avatar_form':avatar_form,
        'information_form':information_form
    }
    return render(request, 'edit_profile.html', context)
