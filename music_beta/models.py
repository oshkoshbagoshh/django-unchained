"""
Church Financial ERP Models

This module contains all models for the church financial ERP system.
Transformed from music/artist portal to church management system.
"""

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
import uuid


def sermon_image_path(instance, filename):
    """
    Generate a unique file path for sermon images to avoid filename collisions.

    Args:
        instance (Model instance): The Sermon model instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path with a UUID as filename inside 'sermons' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('sermons', filename)


def sermon_series_cover_path(instance, filename):
    """
    Generate a unique file path for sermon series cover images.

    Args:
        instance (Model instance): The SermonSeries model instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path with a UUID as filename inside 'sermon_series' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('sermon_series', filename)


def media_item_path(instance, filename):
    """
    Generate a unique file path for media items (PDFs, images, videos).

    Args:
        instance (Model instance): The MediaItem model instance.
        filename (str): The original filename of the uploaded file.

    Returns:
        str: The file path with a UUID as filename inside 'media_items' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('media_items', filename)


def event_image_path(instance, filename):
    """
    Generate a unique file path for event images.

    Args:
        instance (Model instance): The Event model instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path with a UUID as filename inside 'events' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('events', filename)


def ad_banner_path(instance, filename):
    """
    Generate a unique file path for advertising banner images.

    Args:
        instance (Model instance): The AdBanner model instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path with a UUID as filename inside 'ad_banners' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('ad_banners', filename)


def gallery_image_path(instance, filename):
    """
    Generate a unique file path for gallery images.

    Args:
        instance (Model instance): The GalleryImage model instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path with a UUID as filename inside 'gallery' directory.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('gallery', filename)


class ServiceRequest(models.Model):
    """
    Represents a request for a service from the user.

    Fields:
        name (str): Name of the person making the request.
        email (str): Email address of the requester.
        company (str): Company/organization name of the requester.
        service_type (str): Type of service requested chosen from predefined options.
        message (str): Optional detailed message concerning the request.
        created_at (datetime): Timestamp when the request was created.
    """
    SERVICE_TYPE_CHOICES = [
        ('ministry_support', 'Ministry Support'),
        ('financial_assistance', 'Financial Assistance'),
        ('event_planning', 'Event Planning'),
        ('media_services', 'Media Services'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=100, blank=True)
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"


class SermonCategory(models.Model):
    """
    Represents a category for sermons (e.g., Sunday Service, Bible Study, Special Event).

    Fields:
        name (str): The category name.
        description (str): Optional description of the category.
    """
    name = models.CharField(max_length=200, help_text='Enter a sermon category (e.g., Sunday Service, Bible Study)')
    description = models.TextField(blank=True, help_text='Optional description of the category')

    def __str__(self):
        return self.name


class Sermon(models.Model):
    """
    Represents a sermon with related information.

    Fields:
        title (str): Sermon title.
        speaker (str): Name of the speaker/preacher.
        date (date): Date the sermon was delivered.
        description (str): Description or notes about the sermon.
        youtube_url (URLField): Optional YouTube video link.
        audio_file (file): Optional audio file of the sermon.
        pdf_file (file): Optional PDF file (bulletin, notes, etc.).
        image (file): Optional image/thumbnail for the sermon.
        category (ForeignKey): Category this sermon belongs to.
        sermon_series (ForeignKey): Optional series this sermon belongs to.
        view_count (int): Number of times the sermon has been viewed.
        last_viewed (datetime): Last viewed timestamp.
    """
    title = models.CharField(max_length=200, help_text='Enter the sermon title')
    speaker = models.CharField(max_length=200, help_text='Name of the speaker/preacher')
    date = models.DateField(help_text='Date the sermon was delivered')
    description = models.TextField(max_length=2000, help_text='Description or notes about the sermon', blank=True)
    youtube_url = models.URLField(blank=True, null=True, help_text='YouTube video link (optional)')
    audio_file = models.FileField(upload_to=media_item_path, help_text='Audio file (optional)', blank=True, null=True)
    pdf_file = models.FileField(upload_to=media_item_path, help_text='PDF file - bulletin, notes, etc. (optional)', blank=True, null=True)
    image = models.FileField(upload_to=sermon_image_path, help_text='Sermon image/thumbnail', blank=True, null=True)
    category = models.ForeignKey(SermonCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='sermons')
    sermon_series = models.ForeignKey('SermonSeries', on_delete=models.SET_NULL, null=True, blank=True, related_name='sermons')
    view_count = models.IntegerField(default=0, help_text='Number of times the sermon has been viewed')
    last_viewed = models.DateTimeField(null=True, blank=True, help_text='When the sermon was last viewed')
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def image_url(self):
        """
        Returns the URL for the sermon image.
        If no image is set or accessible, returns a fallback placeholder image URL.

        Returns:
            str: URL to the sermon image or a fallback image.
        """
        if self.image and hasattr(self.image, 'url'):
            try:
                _ = self.image.url
                return self.image.url
            except Exception:
                pass
        return f'https://picsum.photos/300?random={self.id}'

    def __str__(self):
        return f"{self.title} - {self.speaker} ({self.date})"


class SermonSeries(models.Model):
    """
    Represents a series of sermons.

    Fields:
        title (str): Series title.
        description (str): Description of the series.
        start_date (date): Start date of the series.
        end_date (date): End date of the series (optional).
        cover_image (file): Cover image for the series.
        category (ForeignKey): Category this series belongs to.
    """
    title = models.CharField(max_length=200, help_text='Enter the series title')
    description = models.TextField(blank=True, help_text='Description of the series')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    cover_image = models.FileField(upload_to=sermon_series_cover_path, help_text='Series cover image', blank=True, null=True)
    category = models.ForeignKey(SermonCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='series')

    @property
    def cover_image_url(self):
        """
        Returns the URL for the series cover image.
        If no image is set or accessible, returns a fallback placeholder image URL.

        Returns:
            str: URL to the series cover image or a fallback image.
        """
        if self.cover_image and hasattr(self.cover_image, 'url'):
            try:
                _ = self.cover_image.url
                return self.cover_image.url
            except Exception:
                pass
        return f'https://picsum.photos/300?random={self.id}'

    def __str__(self):
        return self.title


class MediaItem(models.Model):
    """
    Represents a media item (PDF, image, video, etc.).

    Fields:
        title (str): Media item title.
        description (str): Description of the media item.
        file (file): The media file (PDF, image, video, etc.).
        file_type (str): Type of file (pdf, image, video, audio).
        sermon (ForeignKey): Optional sermon this media item is associated with.
        event (ForeignKey): Optional event this media item is associated with.
        created_at (datetime): When the media item was created.
    """
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200, help_text='Enter the media item title')
    description = models.TextField(blank=True, help_text='Description of the media item')
    file = models.FileField(upload_to=media_item_path, help_text='Media file')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, default='other')
    sermon = models.ForeignKey(Sermon, on_delete=models.SET_NULL, null=True, blank=True, related_name='media_items')
    event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True, related_name='media_items')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Event(models.Model):
    """
    Represents a church event.

    Fields:
        title (str): Event title.
        description (str): Description of the event.
        start_date (datetime): Start date and time of the event.
        end_date (datetime): End date and time of the event (optional).
        location (str): Location of the event.
        image (file): Optional image for the event.
        is_featured (bool): Whether this event should be featured.
        registration_required (bool): Whether registration is required.
        registration_url (URLField): Optional registration URL.
        created_at (datetime): When the event was created.
    """
    title = models.CharField(max_length=200, help_text='Enter the event title')
    description = models.TextField(help_text='Description of the event')
    start_date = models.DateTimeField(help_text='Start date and time of the event')
    end_date = models.DateTimeField(null=True, blank=True, help_text='End date and time of the event (optional)')
    location = models.CharField(max_length=200, help_text='Location of the event')
    image = models.FileField(upload_to=event_image_path, help_text='Event image', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text='Whether this event should be featured')
    registration_required = models.BooleanField(default=False, help_text='Whether registration is required')
    registration_url = models.URLField(blank=True, null=True, help_text='Registration URL (optional)')
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def image_url(self):
        """
        Returns the URL for the event image.
        If no image is set or accessible, returns a fallback placeholder image URL.

        Returns:
            str: URL to the event image or a fallback image.
        """
        if self.image and hasattr(self.image, 'url'):
            try:
                _ = self.image.url
                return self.image.url
            except Exception:
                pass
        return f'https://picsum.photos/300?random={self.id}'

    def __str__(self):
        return f"{self.title} - {self.start_date}"


class ImageGallery(models.Model):
    """
    Represents an image gallery.

    Fields:
        title (str): Gallery title.
        description (str): Description of the gallery.
        created_at (datetime): When the gallery was created.
    """
    title = models.CharField(max_length=200, help_text='Enter the gallery title')
    description = models.TextField(blank=True, help_text='Description of the gallery')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    """
    Represents an image in a gallery.

    Fields:
        gallery (ForeignKey): Gallery this image belongs to.
        image (file): The image file.
        caption (str): Optional caption for the image.
        order (int): Display order within the gallery.
        created_at (datetime): When the image was added.
    """
    gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to=gallery_image_path, help_text='Gallery image')
    caption = models.CharField(max_length=200, blank=True, help_text='Optional caption for the image')
    order = models.IntegerField(default=0, help_text='Display order within the gallery')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.gallery.title} - Image {self.order}"


class Form(models.Model):
    """
    Represents a form that can be filled out by users.

    Fields:
        title (str): Form title.
        description (str): Description of the form.
        form_type (str): Type of form (contact, registration, prayer_request, etc.).
        is_active (bool): Whether the form is currently active.
        created_at (datetime): When the form was created.
    """
    FORM_TYPE_CHOICES = [
        ('contact', 'Contact Form'),
        ('registration', 'Registration Form'),
        ('prayer_request', 'Prayer Request'),
        ('volunteer', 'Volunteer Application'),
        ('donation', 'Donation Form'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200, help_text='Enter the form title')
    description = models.TextField(blank=True, help_text='Description of the form')
    form_type = models.CharField(max_length=20, choices=FORM_TYPE_CHOICES, default='contact')
    is_active = models.BooleanField(default=True, help_text='Whether the form is currently active')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class FormSubmission(models.Model):
    """
    Represents a submission of a form.

    Fields:
        form (ForeignKey): The form that was submitted.
        submitted_by (ForeignKey): User who submitted the form (optional).
        data (JSONField): Form submission data.
        created_at (datetime): When the form was submitted.
    """
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='submissions')
    submitted_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='form_submissions')
    data = models.JSONField(default=dict, help_text='Form submission data')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.form.title} - {self.created_at}"


class AdBanner(models.Model):
    """
    Represents an advertising banner.

    Fields:
        title (str): Banner title.
        image (file): Banner image.
        link_url (URLField): Optional URL to link to when banner is clicked.
        is_active (bool): Whether the banner is currently active.
        start_date (date): Start date for displaying the banner.
        end_date (date): End date for displaying the banner (optional).
        display_order (int): Display order for multiple banners.
        created_at (datetime): When the banner was created.
    """
    title = models.CharField(max_length=200, help_text='Enter the banner title')
    image = models.FileField(upload_to=ad_banner_path, help_text='Banner image')
    link_url = models.URLField(blank=True, null=True, help_text='URL to link to when banner is clicked (optional)')
    is_active = models.BooleanField(default=True, help_text='Whether the banner is currently active')
    start_date = models.DateField(default=timezone.now, help_text='Start date for displaying the banner')
    end_date = models.DateField(null=True, blank=True, help_text='End date for displaying the banner (optional)')
    display_order = models.IntegerField(default=0, help_text='Display order for multiple banners')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.

    This model inherits all the authentication functionality from Django's built-in User model
    while adding custom fields for our application.

    Fields (inherited from AbstractUser):
        username (str): Unique username of the user.
        email (str): Email address.
        password (str): Hashed user password.
        first_name (str): User's first name.
        last_name (str): User's last name.
        is_active (bool): Whether the user account is active.
        is_staff (bool): Whether the user can access the admin site.
        is_superuser (bool): Whether the user has all permissions.
        date_joined (datetime): Timestamp user registered.
        last_login (datetime): Timestamp of the user's last login.

    Additional Fields:
        agreed_to_terms (bool): Whether user agreed to terms and conditions.
        agreed_to_privacy (bool): Whether user agreed to privacy policy.
        receive_marketing (bool): Whether user opted to receive marketing emails.
        agreement_date (datetime): Timestamp when user agreed to terms/privacy policies.
        user_type (str): Type of user - 'member', 'staff', or 'admin'.
    """
    USER_TYPE_CHOICES = [
        ('member', 'Member'),
        ('staff', 'Staff'),
        ('admin', 'Administrator'),
    ]

    # Make email required and unique
    email = models.EmailField(unique=True)

    # Custom fields
    agreed_to_terms = models.BooleanField(default=False, help_text='User has agreed to Terms and Conditions')
    agreed_to_privacy = models.BooleanField(default=False, help_text='User has agreed to Privacy Policy')
    receive_marketing = models.BooleanField(default=False, help_text='User has opted in to marketing emails')
    agreement_date = models.DateTimeField(null=True, blank=True, help_text='When the user agreed to terms')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='member', 
                                help_text='Type of user - member, staff, or admin')


# Financial Models

class FinancialCategory(models.Model):
    """
    Represents a category for financial transactions (income or expense).

    Fields:
        name (str): Category name.
        description (str): Optional description.
        category_type (str): 'income' or 'expense'.
        parent (ForeignKey): Optional parent category for hierarchical organization.
    """
    CATEGORY_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    name = models.CharField(max_length=200, help_text='Category name')
    description = models.TextField(blank=True, help_text='Optional description')
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES, help_text='Income or Expense')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"{self.get_category_type_display()} - {self.name}"


class Donation(models.Model):
    """
    Represents a donation/contribution.

    Fields:
        donor_name (str): Name of the donor.
        donor_email (EmailField): Email of the donor (optional).
        amount (Decimal): Donation amount.
        donation_date (date): Date of the donation.
        payment_method (str): Method of payment (cash, check, card, online, etc.).
        category (ForeignKey): Financial category for this donation.
        notes (str): Optional notes about the donation.
        is_recurring (bool): Whether this is a recurring donation.
        created_at (datetime): When the donation record was created.
        created_by (ForeignKey): User who created this record.
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('card', 'Credit/Debit Card'),
        ('online', 'Online Payment'),
        ('other', 'Other'),
    ]

    donor_name = models.CharField(max_length=200, help_text='Name of the donor')
    donor_email = models.EmailField(blank=True, null=True, help_text='Email of the donor (optional)')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Donation amount')
    donation_date = models.DateField(default=timezone.now, help_text='Date of the donation')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    category = models.ForeignKey(FinancialCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    notes = models.TextField(blank=True, help_text='Optional notes about the donation')
    is_recurring = models.BooleanField(default=False, help_text='Whether this is a recurring donation')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations_created')

    def __str__(self):
        return f"{self.donor_name} - ${self.amount} - {self.donation_date}"


class Expense(models.Model):
    """
    Represents an expense.

    Fields:
        description (str): Description of the expense.
        amount (Decimal): Expense amount.
        expense_date (date): Date of the expense.
        vendor (str): Vendor/supplier name (optional).
        category (ForeignKey): Financial category for this expense.
        receipt (file): Optional receipt file.
        notes (str): Optional notes about the expense.
        created_at (datetime): When the expense record was created.
        created_by (ForeignKey): User who created this record.
    """
    description = models.CharField(max_length=200, help_text='Description of the expense')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Expense amount')
    expense_date = models.DateField(default=timezone.now, help_text='Date of the expense')
    vendor = models.CharField(max_length=200, blank=True, help_text='Vendor/supplier name (optional)')
    category = models.ForeignKey(FinancialCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    receipt = models.FileField(upload_to='expense_receipts/', blank=True, null=True, help_text='Optional receipt file')
    notes = models.TextField(blank=True, help_text='Optional notes about the expense')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses_created')

    def __str__(self):
        return f"{self.description} - ${self.amount} - {self.expense_date}"


class Budget(models.Model):
    """
    Represents a budget for a specific period and category.

    Fields:
        name (str): Budget name/description.
        category (ForeignKey): Financial category this budget is for.
        amount (Decimal): Budgeted amount.
        start_date (date): Start date of the budget period.
        end_date (date): End date of the budget period.
        notes (str): Optional notes about the budget.
        created_at (datetime): When the budget was created.
        created_by (ForeignKey): User who created this budget.
    """
    name = models.CharField(max_length=200, help_text='Budget name/description')
    category = models.ForeignKey(FinancialCategory, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Budgeted amount')
    start_date = models.DateField(help_text='Start date of the budget period')
    end_date = models.DateField(help_text='End date of the budget period')
    notes = models.TextField(blank=True, help_text='Optional notes about the budget')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='budgets_created')

    def __str__(self):
        return f"{self.name} - ${self.amount} ({self.start_date} to {self.end_date})"
