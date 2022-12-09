from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from base.models import Post
from .forms import ProfileForm, UserForm
from .models import Profile
from base.views import get_pre_url

# Create your views here.


@login_required(login_url='login')
def profile(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user)
    followers = user.followers.all()
    following = user_profile.following.all()

    return render(request, 'user_profile/profile.html', {
        'user_profile': user_profile,
        'posts': posts,
        'title': username,
        'followers': followers,
        'following': following
    })


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=True)
            username = user_form.cleaned_data['username']
            user.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile', username=username)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user_profile/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Edit profile'
    })


def follow(request):
    follower = request.user.profile
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    if user in follower.following.all():
        follower.following.remove(user)
        follower.save()
        return redirect(get_pre_url(request))
    else:
        follower.following.add(user)
        follower.save()
        return redirect(get_pre_url(request))
