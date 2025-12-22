# Church Financial ERP System

A comprehensive Django-based ERP system for church management, including content management, financial tracking, and member management.

## Overview

This project has been transformed from a music/artist portal into a church financial ERP system. It provides:

- **Content Management**: Sermons, events, image galleries, forms, and advertising banners
- **Financial Management**: Donations, expenses, budgets, and financial reporting
- **User Management**: Member, staff, and admin user types with role-based access

## Features

### Content Management
- **Sermons**: Upload sermons with YouTube links, PDFs, audio files, and images
- **Sermon Series**: Organize sermons into series
- **Events**: Manage church events with registration, dates, and locations
- **Image Galleries**: Create and manage image galleries
- **Forms**: Contact forms, registration forms, prayer requests, and more
- **Advertising Banners**: Display banners with scheduling and links

### Financial Management
- **Donations**: Track donations with donor information, payment methods, and categories
- **Expenses**: Record expenses with receipts, vendors, and categories
- **Budgets**: Create and manage budgets for specific periods and categories
- **Financial Dashboard**: Overview of financial status (staff/admin only)
- **Financial Categories**: Organize income and expenses by category

### User Management
- **User Types**: 
  - Members: Regular church members
  - Staff: Church staff with financial access
  - Administrators: Full system access
- **Authentication**: Secure user authentication with role-based permissions

## File Upload Functionality

This project supports file uploads for various media types:

### Supported Upload Types
- **Sermon Images**: Upload images for sermons
- **Sermon Series Covers**: Upload cover images for sermon series
- **Media Items**: Upload PDFs, images, videos, and audio files
- **Event Images**: Upload images for events
- **Gallery Images**: Upload images for galleries
- **Ad Banners**: Upload banner images
- **Expense Receipts**: Upload receipts for expenses

### Where Uploads Go
All uploaded files are stored in the `media/` directory at the project root, organized in subdirectories:
- Sermon images: `media/sermons/`
- Sermon series covers: `media/sermon_series/`
- Media items: `media/media_items/`
- Event images: `media/events/`
- Gallery images: `media/gallery/`
- Ad banners: `media/ad_banners/`
- Expense receipts: `media/expense_receipts/`

Files are automatically renamed using UUID to prevent filename conflicts.

## Installation

### Dependencies
- Django >= 5.2.1
- Django REST Framework ~= 3.16.0
- Faker >= 19.3.0 (for generating fake data)
- requests >= 2.31.0
- python-dotenv >= 1.0.0
- reportlab ~= 4.4.1

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file in the project root:
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

The system provides REST API endpoints for all models:

- `/api/sermons/` - Sermons
- `/api/sermon-series/` - Sermon series
- `/api/sermon-categories/` - Sermon categories
- `/api/events/` - Events
- `/api/image-galleries/` - Image galleries
- `/api/gallery-images/` - Gallery images
- `/api/forms/` - Forms
- `/api/form-submissions/` - Form submissions
- `/api/ad-banners/` - Ad banners
- `/api/media-items/` - Media items
- `/api/donations/` - Donations (authenticated)
- `/api/expenses/` - Expenses (authenticated)
- `/api/budgets/` - Budgets (staff/admin only)
- `/api/financial-categories/` - Financial categories
- `/api/users/` - Users

## User Types and Permissions

### Members
- Can view sermons, events, and galleries
- Can submit forms
- Cannot access financial data

### Staff
- All member permissions
- Can view and manage financial data (donations, expenses, budgets)
- Can create and edit content

### Administrators
- Full system access
- Can manage users
- Can access all features

## Email Configuration

All form submissions are sent to the development email specified in settings.py. By default, this is set to `developer@tfnms.co`.

The email backend is set to console backend for development, so emails will be printed to the console instead of being sent.

To change the development email, update the `DEVELOPER_EMAIL` setting in `tfn_ctv/settings.py`.

## Testing

**Note**: Test files (`tests.py`, `test_api.py`) and the fake data generation command (`generate_fake_data.py`) still reference old models and need to be updated for the new church ERP models.

To update tests:
1. Update `music_beta/tests.py` to use new models (Sermon, Event, etc.)
2. Update `music_beta/test_api.py` to use new API endpoints
3. Update `music_beta/management/commands/generate_fake_data.py` to generate church ERP data

## Development

### Project Structure
- `music_beta/` - Main application (content and financial management)
- `tfn_ctv/` - Project settings and configuration
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `media/` - Uploaded media files

### Key Files
- `music_beta/models.py` - All data models
- `music_beta/views.py` - View functions
- `music_beta/admin.py` - Django admin configuration
- `music_beta/forms.py` - Form classes
- `music_beta/api.py` - REST API viewsets
- `music_beta/serializers.py` - API serializers

## Transformation Notes

This project was transformed from a music/artist portal. See `TRANSFORMATION_SUMMARY.md` for detailed information about the changes made.

## License

[Add your license information here]

## Support

For issues or questions, please contact the development team.
