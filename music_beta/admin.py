"""
Django Admin Configuration for Church ERP

This module registers all models with the Django admin interface.
"""

from django.contrib import admin
from .models import (
    ServiceRequest, SermonCategory, Sermon, SermonSeries, MediaItem,
    Event, ImageGallery, GalleryImage, Form, FormSubmission, AdBanner,
    User, FinancialCategory, Donation, Expense, Budget
)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'service_type', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('name', 'email', 'company')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(SermonCategory)
class SermonCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'date', 'category', 'sermon_series', 'view_count')
    list_filter = ('category', 'sermon_series', 'date')
    search_fields = ('title', 'speaker', 'description')
    date_hierarchy = 'date'
    ordering = ('-date', 'title')
    readonly_fields = ('view_count', 'last_viewed', 'created_at')


@admin.register(SermonSeries)
class SermonSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'category')
    list_filter = ('category', 'start_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
    ordering = ('-start_date', 'title')


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'sermon', 'event', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'is_featured', 'registration_required')
    list_filter = ('is_featured', 'registration_required', 'start_date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_date'
    ordering = ('-start_date', 'title')
    readonly_fields = ('created_at',)


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('gallery', 'caption', 'order', 'created_at')
    list_filter = ('gallery', 'created_at')
    search_fields = ('caption',)
    ordering = ('gallery', 'order', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('title', 'form_type', 'is_active', 'created_at')
    list_filter = ('form_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('form', 'submitted_by', 'created_at')
    list_filter = ('form', 'created_at')
    search_fields = ('form__title', 'submitted_by__username', 'submitted_by__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(AdBanner)
class AdBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'start_date', 'end_date', 'display_order')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title',)
    ordering = ('display_order', '-created_at')
    readonly_fields = ('created_at',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'date_joined', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login')


# Financial Admin

@admin.register(FinancialCategory)
class FinancialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'parent')
    list_filter = ('category_type',)
    search_fields = ('name', 'description')
    ordering = ('category_type', 'name')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'donation_date', 'payment_method', 'category', 'is_recurring')
    list_filter = ('payment_method', 'category', 'is_recurring', 'donation_date')
    search_fields = ('donor_name', 'donor_email', 'notes')
    date_hierarchy = 'donation_date'
    ordering = ('-donation_date',)
    readonly_fields = ('created_at',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'expense_date', 'vendor', 'category')
    list_filter = ('category', 'expense_date')
    search_fields = ('description', 'vendor', 'notes')
    date_hierarchy = 'expense_date'
    ordering = ('-expense_date',)
    readonly_fields = ('created_at',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'amount', 'start_date', 'end_date')
    list_filter = ('category', 'start_date', 'end_date')
    search_fields = ('name', 'notes')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    readonly_fields = ('created_at',)
