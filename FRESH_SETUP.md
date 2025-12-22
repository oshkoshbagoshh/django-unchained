# Fresh Setup Guide - Church Financial ERP with Wagtail CMS

This guide will help you set up a fresh Django project with Wagtail CMS for the church financial ERP system.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Update Settings

The settings.py has been updated to use Wagtail CMS instead of Django CMS.

## Step 3: Run Migrations

```bash
python manage.py migrate
```

## Step 4: Create Wagtail Site

```bash
python manage.py createsuperuser
python manage.py wagtail_start
```

## Step 5: Create Initial Content Models

The church ERP models will be integrated with Wagtail pages for content management.

## Features

- **Wagtail CMS**: Modern, flexible CMS for content management
- **Church ERP Models**: Sermons, Events, Financial tracking
- **Wagtail Pages**: Blog posts, sermon pages, event pages
- **Financial Management**: Donations, expenses, budgets
- **User Management**: Member, staff, admin roles

