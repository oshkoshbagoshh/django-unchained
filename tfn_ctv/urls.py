"""
URL configuration for Church Financial ERP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    # Django admin
    path('django-admin/', admin.site.urls),
    
    # Wagtail admin
    path('admin/', include(wagtailadmin_urls)),
    
    # Wagtail documents
    path('documents/', include(wagtaildocs_urls)),
    
    # Church ERP URLs
    path('', include('church_erp.urls')),
    
    # Wagtail pages (must be last)
    path('', include(wagtail_urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
