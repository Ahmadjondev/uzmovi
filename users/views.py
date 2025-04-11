from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ProfileUpdateForm, UserUpdateForm
from movies.models import Watchlist, Rating, Comment

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Get user activity
    watchlist = Watchlist.objects.filter(user=request.user).order_by('-added_at')[:5]
    ratings = Rating.objects.filter(user=request.user).order_by('-created_at')[:5]
    comments = Comment.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'u_form': u_form,
        'form': p_form,
        'watchlist': watchlist,
        'ratings': ratings,
        'comments': comments
    }
    return render(request, 'users/profile.html', context)

@login_required
def user_settings(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your settings have been updated!')
            return redirect('user_settings')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'form': p_form
    }
    return render(request, 'users/settings.html', context)
