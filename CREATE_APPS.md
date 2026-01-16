# Creating New Apps for Fresh Start

## Manual App Creation

Since we're starting fresh, create these apps manually:

### 1. Create church_erp directory structure:

```
church_erp/
    __init__.py
    admin.py
    apps.py
    models.py
    views.py
    urls.py
    forms.py
    serializers.py
    api.py
    migrations/
        __init__.py
```

### 2. Create church_portal directory structure:

```
church_portal/
    __init__.py
    admin.py
    apps.py
    models.py
    views.py
    urls.py
    forms.py
    migrations/
        __init__.py
```

### 3. Create wagtail_pages directory structure:

```
wagtail_pages/
    __init__.py
    admin.py
    apps.py
    models.py
    views.py
    migrations/
        __init__.py
```

## Next Steps

1. Copy models from `music_beta/models.py` to `church_erp/models.py` and update
2. Create Wagtail page models in `wagtail_pages/models.py`
3. Update settings.py to use new apps
4. Run migrations

## Quick Start Commands

After creating the directories:

```bash
# Install dependencies first
pip install -r requirements.txt

# Then update settings.py to reference new apps
# Then run migrations
python manage.py makemigrations
python manage.py migrate
```

