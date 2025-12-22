"""
REST Framework API Viewsets for Church ERP

This module contains API endpoints for all models in the church ERP system.
"""

from rest_framework import viewsets, permissions
from .models import (
    ServiceRequest, SermonCategory, Sermon, SermonSeries, MediaItem,
    Event, ImageGallery, GalleryImage, Form, FormSubmission, AdBanner,
    User, FinancialCategory, Donation, Expense, Budget
)
from .serializers import (
    ServiceRequestSerializer, SermonCategorySerializer, SermonSerializer, 
    SermonSeriesSerializer, MediaItemSerializer, EventSerializer,
    ImageGallerySerializer, GalleryImageSerializer, FormSerializer,
    FormSubmissionSerializer, AdBannerSerializer, UserSerializer,
    FinancialCategorySerializer, DonationSerializer, ExpenseSerializer, BudgetSerializer
)


class ServiceRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows service requests to be viewed or edited.
    """
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAdminUser]


class SermonCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sermon categories to be viewed or edited.
    """
    queryset = SermonCategory.objects.all()
    serializer_class = SermonCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SermonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sermons to be viewed or edited.
    """
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SermonSeriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sermon series to be viewed or edited.
    """
    queryset = SermonSeries.objects.all()
    serializer_class = SermonSeriesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MediaItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows media items to be viewed or edited.
    """
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ImageGalleryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows image galleries to be viewed or edited.
    """
    queryset = ImageGallery.objects.all()
    serializer_class = ImageGallerySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GalleryImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows gallery images to be viewed or edited.
    """
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FormViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows forms to be viewed or edited.
    """
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FormSubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows form submissions to be viewed or edited.
    """
    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AdBannerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ad banners to be viewed or edited.
    """
    queryset = AdBanner.objects.filter(is_active=True)
    serializer_class = AdBannerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Users can only access their own data unless they are admin.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Filter queryset to return only the current user's data unless the user is admin.
        """
        user_id = self.request.session.get('user_id')
        if not user_id:
            return User.objects.none()

        # Check if user is admin
        try:
            user = User.objects.get(id=user_id)
            if user.is_staff or user.is_superuser or user.user_type == 'admin':
                return User.objects.all()
        except User.DoesNotExist:
            pass

        # Regular users can only see their own data
        return User.objects.filter(id=user_id)

    def get_permissions(self):
        """
        Custom permissions:
        - List/Retrieve: Allow if user is authenticated and requesting their own data
        - Create/Update/Delete: Admin only
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


# Financial ViewSets

class FinancialCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows financial categories to be viewed or edited.
    """
    queryset = FinancialCategory.objects.all()
    serializer_class = FinancialCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class DonationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows donations to be viewed or edited.
    """
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        Staff and admins can see all donations, members can only see their own.
        """
        user_id = self.request.session.get('user_id')
        if not user_id:
            return Donation.objects.none()

        try:
            user = User.objects.get(id=user_id)
            if user.is_staff or user.is_superuser or user.user_type in ['admin', 'staff']:
                return Donation.objects.all()
        except User.DoesNotExist:
            pass

        # Members can only see donations they created
        return Donation.objects.filter(created_by_id=user_id)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows expenses to be viewed or edited.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        Staff and admins can see all expenses, members can only see their own.
        """
        user_id = self.request.session.get('user_id')
        if not user_id:
            return Expense.objects.none()

        try:
            user = User.objects.get(id=user_id)
            if user.is_staff or user.is_superuser or user.user_type in ['admin', 'staff']:
                return Expense.objects.all()
        except User.DoesNotExist:
            pass

        # Members can only see expenses they created
        return Expense.objects.filter(created_by_id=user_id)


class BudgetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows budgets to be viewed or edited.
    """
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        Only staff and admins can view budgets.
        """
        user_id = self.request.session.get('user_id')
        if not user_id:
            return Budget.objects.none()

        try:
            user = User.objects.get(id=user_id)
            if user.is_staff or user.is_superuser or user.user_type in ['admin', 'staff']:
                return Budget.objects.all()
        except User.DoesNotExist:
            pass

        # Members cannot view budgets
        return Budget.objects.none()
