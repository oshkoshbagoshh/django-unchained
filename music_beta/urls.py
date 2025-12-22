"""
URL Configuration for Church ERP App

This module defines URL patterns for the church ERP application.
"""

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api import (
    ServiceRequestViewSet, SermonCategoryViewSet, SermonViewSet, 
    SermonSeriesViewSet, MediaItemViewSet, EventViewSet,
    ImageGalleryViewSet, GalleryImageViewSet, FormViewSet,
    FormSubmissionViewSet, AdBannerViewSet, UserViewSet,
    FinancialCategoryViewSet, DonationViewSet, ExpenseViewSet, BudgetViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'service-requests', ServiceRequestViewSet)
router.register(r'sermon-categories', SermonCategoryViewSet)
router.register(r'sermons', SermonViewSet)
router.register(r'sermon-series', SermonSeriesViewSet)
router.register(r'media-items', MediaItemViewSet)
router.register(r'events', EventViewSet)
router.register(r'image-galleries', ImageGalleryViewSet)
router.register(r'gallery-images', GalleryImageViewSet)
router.register(r'forms', FormViewSet)
router.register(r'form-submissions', FormSubmissionViewSet)
router.register(r'ad-banners', AdBannerViewSet)
router.register(r'users', UserViewSet)
router.register(r'financial-categories', FinancialCategoryViewSet)
router.register(r'donations', DonationViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'budgets', BudgetViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('sermons/', views.sermons_list, name='sermons_list'),
    path('sermon/<int:sermon_id>/', views.sermon_detail, name='sermon_detail'),
    path('events/', views.events_list, name='events_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('galleries/', views.galleries_list, name='galleries_list'),
    path('gallery/<int:gallery_id>/', views.gallery_detail, name='gallery_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),
    path('service-request/', views.service_request, name='service_request'),
    
    # Financial URLs (staff/admin only)
    path('financial/donations/', views.donations_list, name='donations_list'),
    path('financial/expenses/', views.expenses_list, name='expenses_list'),
    path('financial/budgets/', views.budgets_list, name='budgets_list'),
    
    # API URLs
    path('api/', include(router.urls)),
]
