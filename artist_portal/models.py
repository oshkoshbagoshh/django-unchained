"""
Member Profile Models for Church ERP

This module contains models for member profiles.
Transformed from artist_portal to member profiles.
"""

from django.db import models
from music_beta.models import User
import uuid
import os


def member_profile_image_path(instance, filename):
    """
    Generate a unique file path for member profile images.

    Args:
        instance (Model instance): The MemberProfile model instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path with a UUID as filename inside 'member_profiles' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('member_profiles', filename)


class MemberProfile(models.Model):
    """
    Represents a church member's profile with additional information.

    Fields:
        user (ForeignKey): The user associated with this profile.
        profile_picture (FileField): The member's profile picture.
        bio (TextField): A detailed biography of the member.
        contact_email (EmailField): Contact email for the member.
        phone (CharField): Contact phone number for the member.
        address (TextField): Member's address.
        facebook (URLField): Member's Facebook profile URL.
        twitter (URLField): Member's Twitter profile URL.
        instagram (URLField): Member's Instagram profile URL.
        website (URLField): Member's website URL.
        ministry_involvement (TextField): Ministries the member is involved in.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    profile_picture = models.FileField(upload_to=member_profile_image_path, blank=True, null=True)
    bio = models.TextField(blank=True, help_text='A brief biography')
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True, help_text='Member address')

    # Social media links
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    website = models.URLField(blank=True)

    # Ministry involvement
    ministry_involvement = models.TextField(blank=True, help_text='Ministries the member is involved in')

    def __str__(self):
        return f"{self.user.username}'s Member Profile"

    @property
    def profile_picture_url(self):
        """
        Returns the URL for the member's profile picture.
        If no image is set or accessible, returns a fallback placeholder image URL.

        Returns:
            str: URL to the member's profile picture or a fallback image.
        """
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            try:
                _ = self.profile_picture.url
                return self.profile_picture.url
            except Exception:
                pass
        return f'https://picsum.photos/300?random={self.user.id}'
