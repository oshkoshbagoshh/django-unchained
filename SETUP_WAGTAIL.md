# Setting Up Church Financial ERP with Wagtail CMS

## Overview
This is a fresh setup using Wagtail CMS for content management and Django for the church financial ERP system.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Create New Apps

Since we're starting fresh, we'll create new apps:

```bash
# Create church_erp app (main ERP functionality)
python manage.py startapp church_erp

# Create church_portal app (member profiles)
python manage.py startapp church_portal

# Create wagtail_pages app (Wagtail page models)
python manage.py startapp wagtail_pages
```

## Step 3: Update Settings

The settings.py has been updated to:
- Use Wagtail CMS instead of Django CMS
- Reference `church_erp` and `church_portal` apps
- Configure Wagtail properly

## Step 4: Create Models

1. **church_erp/models.py**: Financial models (Donation, Expense, Budget) and User model
2. **wagtail_pages/models.py**: Wagtail page models for:
   - SermonPage (extends Wagtail Page)
   - EventPage (extends Wagtail Page)
   - BlogPage (extends Wagtail Page)
   - HomePage (extends Wagtail Page)

## Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 6: Create Wagtail Site

```bash
python manage.py createsuperuser
```

Then in the Wagtail admin:
1. Go to Settings > Sites
2. Create a new site
3. Set the root page

## Step 7: Create Initial Pages

In Wagtail admin, create:
- Home page
- Sermon pages
- Event pages
- Blog pages

## Features

### Wagtail CMS Integration
- **Sermon Pages**: Rich content pages for sermons with YouTube embeds, PDFs, audio
- **Event Pages**: Event pages with dates, locations, registration
- **Blog Pages**: General blog/content pages
- **Home Page**: Customizable home page

### Financial Management
- Donations tracking
- Expenses tracking
- Budget management
- Financial categories
- Financial dashboard (staff/admin only)

### User Management
- Member profiles
- Staff access
- Admin access
- Role-based permissions

## Next Steps

1. Create the new app directories
2. Move/update models from music_beta to church_erp
3. Create Wagtail page models
4. Update templates to use Wagtail
5. Test the setup

