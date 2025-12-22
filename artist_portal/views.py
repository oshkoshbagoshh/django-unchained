"""
Views for Member Profiles

This module contains views for member profile management.
Transformed from artist_portal to member profiles.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from music_beta.models import User
from .models import MemberProfile
from .forms import MemberProfileForm


def member_profile(request):
    """
    View function for the member's profile page.
    Accessible to all authenticated users.
    """
    # Check if user is logged in
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to view your profile.')
        return redirect('login')

    user = request.user

    # Get or create member profile
    profile, created = MemberProfile.objects.get_or_create(user=user)

    # Handle form submission
    if request.method == 'POST':
        form = MemberProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('member_profile')
    else:
        form = MemberProfileForm(instance=profile)

    context = {
        'user': user,
        'profile': profile,
        'form': form,
    }

    return render(request, 'artist_portal/member_profile.html', context)


def member_public_profile(request, username):
    """
    View function for the public view of a member's profile.
    Accessible to all users.
    """
    user = get_object_or_404(User, username=username)
    profile = MemberProfile.objects.filter(user=user).first()

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'artist_portal/member_public_profile.html', context)
