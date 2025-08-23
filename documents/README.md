# Car Zone - Django Admin Setup

A comprehensive Django application for managing a car marketplace with a fully-featured admin interface.

## 🚀 Quick Start

1. **Activate Virtual Environment**

   ```bash
   cd backend
   source venv/Scripts/activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**

   ```bash
   cd src
   python manage.py migrate
   ```

4. **Seed Database (Optional)**

   ```bash
   cd ..
   python seed_database.py
   ```

5. **Start Server**

   ```bash
   cd src
   python manage.py runserver
   ```

6. **Access Admin**
   - URL: http://127.0.0.1:8000/admin/
   - Username: `shafi`
   - Password: `shafi`

## 📊 Features

- **User Management**: Buyers, sellers, and admin roles
- **Car Listings**: Complete car marketplace functionality
- **Messaging**: Communication between buyers and sellers
- **Moderation**: Report system for content moderation
- **Analytics**: Search logs and daily metrics
- **Admin Interface**: Comprehensive Django admin with custom features

## 🗄️ Database Models

- **Users**: 11 sample users with different roles
- **Cars**: 10 different car models
- **Listings**: 10 car listings with various statuses
- **Messages**: 11 conversations between users
- **Reports**: 7 moderation reports
- **Analytics**: 7 days of sample analytics data

## 📚 Documentation

See [ADMIN_SETUP.md](ADMIN_SETUP.md) for detailed documentation.

## 🛠️ Tech Stack

- Django 5.2.5
- PostgreSQL
- Django REST Framework 3.16.1
- Pillow (for image handling)

## 📁 Project Structure

```
backend/
├── src/
│   ├── accounts/          # User management
│   ├── cars/              # Car and listing models
│   ├── messaging/         # Message system
│   ├── moderation/        # Report system
│   ├── analytics/         # Analytics and search logs
│   └── carzone/           # Project settings
├── venv/                  # Virtual environment
├── requirements.txt       # Dependencies
├── seed_database.py       # Sample data generator
└── ADMIN_SETUP.md        # Detailed documentation
```

## 🎯 Admin Highlights

- **Enhanced User Admin**: Role-based filtering, profile pictures
- **Car Management**: Inline listings, bulk actions
- **Message Tracking**: Read/unread status, conversation threads
- **Report Moderation**: Status workflow, admin assignments
- **Analytics Dashboard**: Daily metrics, search insights

## 🔧 Development

The admin interface is fully configured with:

- Custom list displays and filters
- Bulk actions for common operations
- Optimized queries for performance
- Rich formatting and cross-references
- Sample data for testing

---

## 🆘 Frequently Asked Questions (FAQ)

### 🔴 Common Issues & Solutions

#### **Q: Django is not found / ModuleNotFoundError**

```bash
# Solution: Activate virtual environment
cd backend
source venv/Scripts/activate  # Git Bash
# OR
venv\Scripts\activate         # Windows CMD

# Verify Django is installed
pip list | grep Django
```

#### **Q: PostgreSQL connection errors**

```bash
# Check if PostgreSQL is running
# Windows: Services -> PostgreSQL
# Or check connection manually:
psql -U shafi -d carzone_db -h localhost -p 5432

# Database credentials (in settings.py):
# NAME: carzone_db
# USER: shafi
# PASSWORD: shafi
# HOST: localhost
# PORT: 5432
```

#### **Q: Migration errors**

```bash
# Step 1: Check for migration conflicts
cd src
python manage.py showmigrations

# Step 2: Reset migrations (CAREFUL - loses data)
python manage.py migrate --fake-initial

# Step 3: If still issues, reset specific app
python manage.py migrate accounts zero
python manage.py migrate accounts

# Step 4: Complete reset (nuclear option)
# Delete all migration files except __init__.py in migrations folders
python manage.py makemigrations
python manage.py migrate
```

---

## 🗄️ Database Management

### **Complete Database Reset**

```bash
# Method 1: Using PostgreSQL commands
cd backend
source venv/Scripts/activate

# Connect to postgres (not carzone_db)
psql -U shafi -d postgres

# In PostgreSQL shell:
DROP DATABASE IF EXISTS carzone_db;
CREATE DATABASE carzone_db OWNER shafi;
\q

# Recreate tables
cd src
python manage.py migrate
```

### **Alternative: Django Database Reset**

```bash
cd backend/src
python manage.py flush  # Removes all data, keeps tables
# OR
python manage.py reset_db  # If django-extensions installed
```

---

## 👤 Superuser Management

### **Create New Superuser**

```bash
cd backend/src
source ../venv/Scripts/activate
python manage.py createsuperuser

# Follow prompts:
# Username: your_username
# Email: your_email@example.com
# Password: your_password
```

### **Reset Existing Superuser Password**

```bash
cd backend/src
python manage.py changepassword shafi
# OR create new superuser with same username (will update)
```

### **Programmatic Superuser Creation**

```bash
cd backend/src
python manage.py shell

# In Django shell:
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='shafi')
user.set_password('new_password')
user.save()
exit()
```

---

## 🌱 Database Seeding

### **Run Seed Script**

```bash
cd backend
source venv/Scripts/activate
python seed_database.py
```

### **Manual Seeding (if script fails)**

```bash
cd backend/src
python manage.py shell

# In Django shell:
exec(open('../seed_database.py').read())
```

### **Clear Seeded Data**

```bash
cd backend/src
python manage.py shell

# In Django shell:
from accounts.models import *
from cars.models import *
from messaging.models import *
from moderation.models import *
from analytics.models import *

# Delete in correct order (due to foreign keys)
Message.objects.all().delete()
Report.objects.all().delete()
Favorite.objects.all().delete()
CarListing.objects.all().delete()
Car.objects.all().delete()
BuyerProfile.objects.all().delete()
SellerProfile.objects.all().delete()
# Keep superuser, delete test users
User.objects.exclude(username='shafi').delete()
```

---

## 🐛 Debugging & Troubleshooting

### **Check Django Configuration**

```bash
cd backend/src
python manage.py check
python manage.py check --deploy  # Production checks
```

### **View Current Migrations**

```bash
python manage.py showmigrations
python manage.py showmigrations accounts  # Specific app
```

### **Database Schema Inspection**

```bash
# Connect to database
psql -U shafi -d carzone_db

# In PostgreSQL:
\dt                    # List all tables
\d accounts_user       # Describe specific table
\du                    # List users
\l                     # List databases
```

### **Django Shell for Testing**

```bash
cd backend/src
python manage.py shell

# Test database connection:
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
```

---

## 🔧 Environment Issues

### **Python Virtual Environment Problems**

```bash
# Recreate virtual environment
cd backend
deactivate  # If already activated
rm -rf venv  # Remove old environment

# Create new environment
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### **Port Already in Use**

```bash
# Find process using port 8000
netstat -ano | findstr :8000  # Windows
# OR
lsof -i :8000  # Linux/Mac

# Kill process (Windows)
taskkill /PID <PID_NUMBER> /F

# Use different port
python manage.py runserver 8001
```

### **Static Files Not Loading**

```bash
# Collect static files
cd backend/src
python manage.py collectstatic

# Check settings.py:
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']

# For development, add to urls.py:
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📦 Dependencies & Updates

### **Update Dependencies**

```bash
cd backend
source venv/Scripts/activate

# Update specific package
pip install --upgrade django

# Update all packages (careful!)
pip list --outdated
pip freeze > requirements_old.txt
pip install --upgrade -r requirements.txt

# Regenerate requirements
pip freeze > requirements.txt
```

### **Add New Dependencies**

```bash
# Install new package
pip install package_name

# Add to requirements
pip freeze > requirements.txt

# Install from requirements (new environment)
pip install -r requirements.txt
```

---

## 🚀 Production Deployment

### **Environment Variables**

```bash
# Create .env file (never commit to git)
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@localhost/dbname
```

### **Production Checklist**

```bash
# Security check
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput

# Create superuser for production
python manage.py createsuperuser

# Test with production-like settings
DEBUG=False python manage.py runserver
```

---

## 📞 Quick Commands Reference

```bash
# Start development
cd backend && source venv/Scripts/activate && cd src && python manage.py runserver

# Reset everything
cd backend && dropdb carzone_db && createdb carzone_db && cd src && python manage.py migrate && cd .. && python seed_database.py

# Create superuser
cd backend/src && python manage.py createsuperuser

# Django shell
cd backend/src && python manage.py shell

# Check status
cd backend/src && python manage.py check

# View migrations
cd backend/src && python manage.py showmigrations

# Database shell
psql -U shafi -d carzone_db
```

---

## 🆘 Emergency Recovery

### **Complete Project Reset**

```bash
# 1. Backup current state (optional)
cp -r backend backend_backup

# 2. Reset database
dropdb carzone_db && createdb carzone_db

# 3. Reset migrations
find backend/src -path "*/migrations/*.py" -not -name "__init__.py" -delete
find backend/src -path "*/migrations/*.pyc" -delete

# 4. Recreate everything
cd backend/src
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 5. Reseed data
cd ..
python seed_database.py
```

### **Git Reset (if version controlled)**

```bash
# Reset to last working commit
git log --oneline  # Find last good commit
git reset --hard <commit_hash>

# Or reset to remote
git fetch origin
git reset --hard origin/main
```

---

## 📱 Contact & Support

- **Admin URL**: http://127.0.0.1:8000/admin/
- **Default Superuser**: `shafi` / `shafi`
- **PostgreSQL Database**: `carzone_db`
- **Django Version**: 5.2.5

### **Useful Links**

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Admin Documentation](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/)

---

_Car Zone Admin - Built with Django_
