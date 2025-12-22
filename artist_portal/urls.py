"""
URL Configuration for Member Profiles

This module defines URL patterns for member profile management.
Transformed from artist_portal to member profiles.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.member_profile, name='member_profile'),
    path('profile/<str:username>/', views.member_public_profile, name='member_public_profile'),
]
