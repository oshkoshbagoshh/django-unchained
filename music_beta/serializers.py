"""
REST Framework Serializers for Church ERP

This module contains serializers for all models in the church ERP system.
"""

from rest_framework import serializers
from .models import (
    ServiceRequest, SermonCategory, Sermon, SermonSeries, MediaItem,
    Event, ImageGallery, GalleryImage, Form, FormSubmission, AdBanner,
    User, FinancialCategory, Donation, Expense, Budget
)


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['id', 'name', 'email', 'company', 'service_type', 'message', 'created_at']


class SermonCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SermonCategory
        fields = '__all__'


class SermonSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=SermonCategory.objects.all(), required=False, allow_null=True)
    sermon_series = serializers.PrimaryKeyRelatedField(queryset=SermonSeries.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Sermon
        fields = ['id', 'title', 'speaker', 'date', 'description', 'youtube_url', 'audio_file', 
                 'pdf_file', 'image', 'image_url', 'category', 'sermon_series', 'view_count', 
                 'last_viewed', 'created_at']


class SermonSeriesSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=SermonCategory.objects.all(), required=False, allow_null=True)

    class Meta:
        model = SermonSeries
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'cover_image', 
                 'cover_image_url', 'category']


class MediaItemSerializer(serializers.ModelSerializer):
    sermon = serializers.PrimaryKeyRelatedField(queryset=Sermon.objects.all(), required=False, allow_null=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False, allow_null=True)

    class Meta:
        model = MediaItem
        fields = ['id', 'title', 'description', 'file', 'file_type', 'sermon', 'event', 'created_at']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'location', 'image', 
                 'image_url', 'is_featured', 'registration_required', 'registration_url', 'created_at']


class GalleryImageSerializer(serializers.ModelSerializer):
    gallery = serializers.PrimaryKeyRelatedField(queryset=ImageGallery.objects.all())

    class Meta:
        model = GalleryImage
        fields = ['id', 'gallery', 'image', 'caption', 'order', 'created_at']


class ImageGallerySerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = ImageGallery
        fields = ['id', 'title', 'description', 'images', 'created_at']


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id', 'title', 'description', 'form_type', 'is_active', 'created_at']


class FormSubmissionSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())
    submitted_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = FormSubmission
        fields = ['id', 'form', 'submitted_by', 'data', 'created_at']


class AdBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdBanner
        fields = ['id', 'title', 'image', 'link_url', 'is_active', 'start_date', 'end_date', 
                 'display_order', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 
                 'agreed_to_terms', 'agreed_to_privacy', 'receive_marketing', 'agreement_date',
                 'user_type', 'is_active', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}


# Financial Serializers

class FinancialCategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=FinancialCategory.objects.all(), required=False, allow_null=True)

    class Meta:
        model = FinancialCategory
        fields = ['id', 'name', 'description', 'category_type', 'parent']


class DonationSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=FinancialCategory.objects.all(), required=False, allow_null=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Donation
        fields = ['id', 'donor_name', 'donor_email', 'amount', 'donation_date', 'payment_method', 
                 'category', 'notes', 'is_recurring', 'created_at', 'created_by']


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=FinancialCategory.objects.all(), required=False, allow_null=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Expense
        fields = ['id', 'description', 'amount', 'expense_date', 'vendor', 'category', 'receipt', 
                 'notes', 'created_at', 'created_by']


class BudgetSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=FinancialCategory.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Budget
        fields = ['id', 'name', 'category', 'amount', 'start_date', 'end_date', 'notes', 
                 'created_at', 'created_by']
