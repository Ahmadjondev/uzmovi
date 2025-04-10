from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm
from movies.models import Watchlist, Rating, Comment

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    # Get user activity
    watchlist = Watchlist.objects.filter(user=request.user).order_by('-added_at')[:5]
    ratings = Rating.objects.filter(user=request.user).order_by('-created_at')[:5]
    comments = Comment.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'form': form,
        'watchlist': watchlist,
        'ratings': ratings,
        'comments': comments
    }
    return render(request, 'users/profile.html', context)

@login_required
def user_settings(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated!')
            return redirect('user_settings')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'form': form
    }
    return render(request, 'users/settings.html', context)
