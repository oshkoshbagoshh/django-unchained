"""
Forms for Church ERP

This module contains all form classes for the church ERP system.
"""

from django import forms
from django.core.validators import RegexValidator
from .models import (
    ServiceRequest, Sermon, SermonSeries, MediaItem, Event,
    ImageGallery, GalleryImage, Form, FormSubmission, AdBanner,
    Donation, Expense, Budget, FinancialCategory
)


class ServiceRequestForm(forms.Form):
    """Form for service requests."""
    name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})
    )
    company = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Organization (optional)'})
    )
    service_type = forms.ChoiceField(
        choices=[
            ('', 'Select Service Type'),
            ('ministry_support', 'Ministry Support'),
            ('financial_assistance', 'Financial Assistance'),
            ('event_planning', 'Event Planning'),
            ('media_services', 'Media Services'),
            ('other', 'Other')
        ], 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}), 
        required=False
    )


class UserSignupForm(forms.Form):
    """Form for user signup."""
    username = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    # User type selection
    user_type = forms.ChoiceField(
        choices=[
            ('member', 'I am a church member'),
            ('staff', 'I am church staff'),
            ('admin', 'I am an administrator')
        ],
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='member'
    )

    # Terms and conditions agreement
    agree_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I agree to the Terms and Conditions and Privacy Policy',
        error_messages={'required': 'You must agree to the Terms and Conditions and Privacy Policy to sign up.'}
    )

    # Marketing emails opt-in
    receive_marketing = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I would like to receive updates about church events and activities'
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        # Ensure terms are agreed to
        if not cleaned_data.get('agree_terms'):
            raise forms.ValidationError("You must agree to the Terms and Conditions and Privacy Policy to sign up.")

        return cleaned_data


class LoginForm(forms.Form):
    """Form for user login."""
    username = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Remember me'
    )


class SermonForm(forms.ModelForm):
    """Form for sermon creation/editing."""
    class Meta:
        model = Sermon
        fields = ['title', 'speaker', 'date', 'description', 'youtube_url', 'audio_file', 
                 'pdf_file', 'image', 'category', 'sermon_series']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sermon Title'}),
            'speaker': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Speaker Name'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'YouTube URL (optional)'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'audio/*'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sermon_series': forms.Select(attrs={'class': 'form-control'}),
        }


class EventForm(forms.ModelForm):
    """Form for event creation/editing."""
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'location', 'image', 
                 'is_featured', 'registration_required', 'registration_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Location'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'registration_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'registration_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Registration URL (optional)'}),
        }


class DonationForm(forms.ModelForm):
    """Form for donation entry."""
    class Meta:
        model = Donation
        fields = ['donor_name', 'donor_email', 'amount', 'donation_date', 'payment_method', 
                 'category', 'notes', 'is_recurring']
        widgets = {
            'donor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Donor Name'}),
            'donor_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Donor Email (optional)'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'donation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ExpenseForm(forms.ModelForm):
    """Form for expense entry."""
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'expense_date', 'vendor', 'category', 'receipt', 'notes']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Expense Description'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'expense_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'vendor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vendor Name (optional)'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'receipt': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,image/*'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BudgetForm(forms.ModelForm):
    """Form for budget creation/editing."""
    class Meta:
        model = Budget
        fields = ['name', 'category', 'amount', 'start_date', 'end_date', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Budget Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
