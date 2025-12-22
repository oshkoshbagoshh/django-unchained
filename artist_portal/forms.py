"""
Forms for Member Profiles

This module contains forms for member profile management.
Transformed from artist_portal to member profiles.
"""

from django import forms
from .models import MemberProfile


class MemberProfileForm(forms.ModelForm):
    """Form for member profile management."""
    class Meta:
        model = MemberProfile
        fields = [
            'profile_picture', 'bio', 'contact_email', 'phone', 'address',
            'facebook', 'twitter', 'instagram', 'website',
            'ministry_involvement'
        ]
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us about yourself'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook Profile URL'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Twitter Profile URL'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Instagram Profile URL'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            'ministry_involvement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ministries you are involved in'}),
        }
