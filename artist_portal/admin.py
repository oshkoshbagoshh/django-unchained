"""
Django Admin Configuration for Member Profiles

This module registers member profile models with the Django admin interface.
"""

from django.contrib import admin
from .models import MemberProfile


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_email', 'phone')
    search_fields = ('user__username', 'user__email', 'contact_email', 'phone')
    list_filter = ('user__user_type',)
    readonly_fields = ('user',)
