"""
Views for Church Financial ERP

This module contains all view functions for the church ERP system.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Sum, Count
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .forms import LoginForm, ServiceRequestForm, UserSignupForm
from .models import (
    User, ServiceRequest, Sermon, SermonSeries, SermonCategory, MediaItem,
    Event, ImageGallery, GalleryImage, Form, FormSubmission, AdBanner,
    FinancialCategory, Donation, Expense, Budget
)
from io import BytesIO
import json
import os


def is_staff_or_admin(user):
    """Check if user is staff or admin."""
    return user.is_authenticated and (user.is_staff or user.user_type in ['admin', 'staff'])


def home(request):
    """
    View function for the home page of the church ERP site.
    """
    # Get featured events
    featured_events = Event.objects.filter(is_featured=True, start_date__gte=timezone.now()).order_by('start_date')[:3]
    
    # Get recent sermons
    recent_sermons = Sermon.objects.all().order_by('-date')[:5]
    
    # Get active banners
    active_banners = AdBanner.objects.filter(
        is_active=True,
        start_date__lte=timezone.now().date()
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=timezone.now().date())
    ).order_by('display_order')[:5]

    signup_form = UserSignupForm()

    context = {
        'signup_form': signup_form,
        'featured_events': featured_events,
        'recent_sermons': recent_sermons,
        'active_banners': active_banners,
    }

    return render(request, 'music_beta/home.html', context)


@csrf_exempt
def signup(request):
    """
    View function for user signup.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            user_type = data.get('user_type', 'member')  # Default to member
            agree_terms = data.get('agree_terms', False)
            receive_marketing = data.get('receive_marketing', False)

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists'})
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already exists'})

            # Check if terms are agreed to
            if not agree_terms:
                return JsonResponse({'success': False, 'message': 'You must agree to the Terms and Conditions and Privacy Policy to sign up.'})

            # Validate user_type
            if user_type not in ['member', 'staff', 'admin']:
                return JsonResponse({'success': False, 'message': 'Invalid user type. Must be member, staff, or admin.'})

            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                agreed_to_terms=True,
                agreed_to_privacy=True,
                receive_marketing=receive_marketing,
                agreement_date=timezone.now()
            )

            # Set up session
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['user_type'] = user.user_type

            return JsonResponse({
                'success': True, 
                'message': 'User created successfully',
                'user_id': user.id,
                'user_type': user.user_type
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt
def search(request):
    """
    View function for search functionality.
    """
    if request.method == 'GET':
        query = request.GET.get('q', '')

        if not query:
            return JsonResponse({'success': False, 'message': 'No search query provided'})

        # Search for sermons, events, and media items
        sermons = Sermon.objects.filter(
            Q(title__icontains=query) | Q(speaker__icontains=query) | Q(description__icontains=query)
        ).values('id', 'title', 'speaker', 'date', 'youtube_url')
        
        events = Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        ).values('id', 'title', 'start_date', 'location')
        
        media_items = MediaItem.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).values('id', 'title', 'file_type')

        results = {
            'sermons': list(sermons),
            'events': list(events),
            'media_items': list(media_items),
        }

        return JsonResponse({'success': True, 'results': results})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def service_request(request):
    """
    View function for handling service requests.
    """
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            # Save the service request to the database
            service_request = ServiceRequest.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                company=form.cleaned_data.get('company', ''),
                service_type=form.cleaned_data['service_type'],
                message=form.cleaned_data['message']
            )

            # Send email notification
            subject = f"New Service Request: {form.cleaned_data['service_type']}"
            message = f"""
            New service request received:

            Name: {form.cleaned_data['name']}
            Email: {form.cleaned_data['email']}
            Company: {form.cleaned_data.get('company', 'N/A')}
            Service Type: {form.cleaned_data['service_type']}
            Message: {form.cleaned_data['message']}
            """
            recipient_email = getattr(settings, 'DEVELOPER_EMAIL', settings.DEFAULT_FROM_EMAIL)
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )

            messages.success(request, 'Your service request has been submitted successfully. We will contact you soon.')
            return redirect('service_request')
    else:
        form = ServiceRequestForm()

    return render(request, 'music_beta/service_request.html', {'form': form})


def sermons_list(request):
    """
    View function for listing all sermons.
    """
    sermons = Sermon.objects.all().order_by('-date')
    categories = SermonCategory.objects.all()
    series = SermonSeries.objects.all()
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        sermons = sermons.filter(category_id=category_id)
    
    # Filter by series if provided
    series_id = request.GET.get('series')
    if series_id:
        sermons = sermons.filter(sermon_series_id=series_id)

    context = {
        'sermons': sermons,
        'categories': categories,
        'series': series,
    }

    return render(request, 'music_beta/sermons_list.html', context)


def sermon_detail(request, sermon_id):
    """
    View function for sermon detail page.
    """
    sermon = get_object_or_404(Sermon, id=sermon_id)
    
    # Update view count
    sermon.view_count += 1
    sermon.last_viewed = timezone.now()
    sermon.save()
    
    # Get related media items
    media_items = MediaItem.objects.filter(sermon=sermon)
    
    # Get other sermons in the same series
    related_sermons = Sermon.objects.filter(sermon_series=sermon.sermon_series).exclude(id=sermon_id).order_by('date')[:5]

    context = {
        'sermon': sermon,
        'media_items': media_items,
        'related_sermons': related_sermons,
    }

    return render(request, 'music_beta/sermon_detail.html', context)


def events_list(request):
    """
    View function for listing all events.
    """
    events = Event.objects.all().order_by('start_date')
    
    # Filter upcoming events
    upcoming = events.filter(start_date__gte=timezone.now())
    
    # Filter past events
    past = events.filter(start_date__lt=timezone.now())

    context = {
        'upcoming_events': upcoming,
        'past_events': past,
    }

    return render(request, 'music_beta/events_list.html', context)


def event_detail(request, event_id):
    """
    View function for event detail page.
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Get related media items
    media_items = MediaItem.objects.filter(event=event)

    context = {
        'event': event,
        'media_items': media_items,
    }

    return render(request, 'music_beta/event_detail.html', context)


def galleries_list(request):
    """
    View function for listing all image galleries.
    """
    galleries = ImageGallery.objects.all().order_by('-created_at')

    context = {
        'galleries': galleries,
    }

    return render(request, 'music_beta/galleries_list.html', context)


def gallery_detail(request, gallery_id):
    """
    View function for gallery detail page.
    """
    gallery = get_object_or_404(ImageGallery, id=gallery_id)
    images = gallery.images.all()

    context = {
        'gallery': gallery,
        'images': images,
    }

    return render(request, 'music_beta/gallery_detail.html', context)


def login_view(request):
    """
    View function for user login.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Update last login time
                user.last_login = timezone.now()
                user.save()

                # Set session expiry if remember_me is checked
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Session expires when browser closes

                messages.success(request, f'Welcome back, {username}!')

                # Redirect based on user type
                if user.user_type == 'admin' or user.is_staff:
                    return redirect('admin:index')
                elif user.user_type == 'staff':
                    return redirect('financial_dashboard')
                else:  # member
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form data.')
    else:
        form = LoginForm()

    return render(request, 'music_beta/login.html', {'form': form})


def logout_view(request):
    """
    View function for user logout.
    """
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# Financial Views (Staff/Admin only)

@login_required
@user_passes_test(is_staff_or_admin)
def donations_list(request):
    """
    View function for listing all donations (staff/admin only).
    """
    donations = Donation.objects.all().order_by('-donation_date')
    
    # Get summary statistics
    total_donations = donations.aggregate(Sum('amount'))['amount__sum'] or 0
    donation_count = donations.count()
    
    # Filter by date range if provided
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        donations = donations.filter(donation_date__gte=start_date)
    if end_date:
        donations = donations.filter(donation_date__lte=end_date)

    context = {
        'donations': donations,
        'total_donations': total_donations,
        'donation_count': donation_count,
    }

    return render(request, 'music_beta/donations_list.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
def expenses_list(request):
    """
    View function for listing all expenses (staff/admin only).
    """
    expenses = Expense.objects.all().order_by('-expense_date')
    
    # Get summary statistics
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    expense_count = expenses.count()
    
    # Filter by date range if provided
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        expenses = expenses.filter(expense_date__gte=start_date)
    if end_date:
        expenses = expenses.filter(expense_date__lte=end_date)

    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'expense_count': expense_count,
    }

    return render(request, 'music_beta/expenses_list.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
def budgets_list(request):
    """
    View function for listing all budgets (staff/admin only).
    """
    budgets = Budget.objects.all().order_by('-start_date')
    
    # Get current budgets
    now = timezone.now().date()
    current_budgets = budgets.filter(start_date__lte=now, end_date__gte=now)

    context = {
        'budgets': budgets,
        'current_budgets': current_budgets,
    }

    return render(request, 'music_beta/budgets_list.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
def financial_dashboard(request):
    """
    View function for financial dashboard (staff/admin only).
    """
    # Get financial summary
    total_donations = Donation.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    net_income = total_donations - total_expenses
    
    # Get recent transactions
    recent_donations = Donation.objects.all().order_by('-donation_date')[:10]
    recent_expenses = Expense.objects.all().order_by('-expense_date')[:10]
    
    # Get current budgets
    now = timezone.now().date()
    current_budgets = Budget.objects.filter(start_date__lte=now, end_date__gte=now)

    context = {
        'total_donations': total_donations,
        'total_expenses': total_expenses,
        'net_income': net_income,
        'recent_donations': recent_donations,
        'recent_expenses': recent_expenses,
        'current_budgets': current_budgets,
    }

    return render(request, 'music_beta/financial_dashboard.html', context)
