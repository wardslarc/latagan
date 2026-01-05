# 🛠️ LATAGAN - Developer Guide

## Complete Django Development Documentation

---

## 🏁 Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Models Explained](#models-explained)
4. [Views & Logic](#views--logic)
5. [URL Routing](#url-routing)
6. [Templates](#templates)
7. [Static Files](#static-files)
8. [Admin Interface](#admin-interface)
9. [Common Tasks](#common-tasks)
10. [Troubleshooting](#troubleshooting)

---

## 🏁 Getting Started

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Initial Setup

```bash
# 1. Navigate to project
cd latagan

# 2. Create virtual environment
python -m venv venv

# 3. Activate it (Windows)
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Populate categories
python manage.py populate_categories

# 8. Run server
python manage.py runserver
```

---

## 📂 Project Structure

### Django Project Layout

```
latagan/
├── manage.py                 # Management CLI
│
├── latagan_project/          # Project settings
│   ├── settings.py          # Configuration
│   ├── urls.py              # Main routing
│   └── wsgi.py              # Production server
│
└── store/                    # Main application
    ├── models.py            # Database models
    ├── views.py             # Request handlers
    ├── urls.py              # App routing
    ├── admin.py             # Admin setup
    ├── apps.py              # App config
    ├── tests.py             # Unit tests
    ├── static/              # CSS, JS, images
    ├── templates/           # HTML templates
    └── migrations/          # Database versions
```

### Key Configuration Files

**settings.py**
```python
# Add apps
INSTALLED_APPS = [
    'store',  # ← Your app
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 🗄️ Models Explained

### The 6 Database Models

#### 1. Category Model
```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    # Use:
    # - Organize products
    # - Filtering on browse page
    # - Navigation menu
```

**Common Queries:**
```python
# Get all categories
categories = Category.objects.all()

# Get specific category
category = Category.objects.get(name='Clothing')

# Count items in category
count = category.item_set.count()
```

#### 2. Item Model
```python
class Item(models.Model):
    seller = ForeignKey(User)
    category = ForeignKey(Category)
    title = CharField(max_length=200)
    description = TextField()
    price = DecimalField()
    image = ImageField()
    condition = CharField()
    status = CharField()  # available, sold, reserved
    created_at = DateTimeField()
    updated_at = DateTimeField()
    
    # Use:
    # - Main product listings
    # - Search & filtering
    # - Shopping cart items
```

**Common Queries:**
```python
# Get all available items
items = Item.objects.filter(status='available')

# Get seller's items
seller_items = Item.objects.filter(seller=user)

# Search items
results = Item.objects.filter(title__icontains='jacket')

# Filter by category
category_items = Item.objects.filter(category_id=1)

# Recent items
recent = Item.objects.order_by('-created_at')[:10]
```

#### 3. UserProfile Model
```python
class UserProfile(models.Model):
    user = OneToOneField(User)
    bio = TextField()
    profile_image = ImageField()
    is_seller = BooleanField()
    rating = DecimalField()
    phone = CharField()
    address = TextField()
    created_at = DateTimeField()
    
    # Use:
    # - Seller information
    # - Ratings & reputation
    # - Contact details
```

**Common Queries:**
```python
# Get user profile
profile = UserProfile.objects.get(user=request.user)

# Find sellers by rating
top_sellers = UserProfile.objects.filter(
    is_seller=True
).order_by('-rating')[:10]

# Update profile
profile.rating = 4.5
profile.save()
```

#### 4. Order Model
```python
class Order(models.Model):
    item = ForeignKey(Item)
    buyer = ForeignKey(User)
    status = CharField()  # pending, confirmed, shipped, delivered
    total_price = DecimalField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    
    # Use:
    # - Purchase records
    # - Order tracking
    # - Transaction history
```

**Common Queries:**
```python
# Get user's orders
my_orders = Order.objects.filter(buyer=request.user)

# Get seller's sales
my_sales = Order.objects.filter(item__seller=request.user)

# Filter by status
shipped = Order.objects.filter(status='shipped')

# Recent orders
recent = Order.objects.order_by('-created_at')[:20]
```

#### 5. Review Model
```python
class Review(models.Model):
    item = ForeignKey(Item)
    author = ForeignKey(User)
    rating = IntegerField()  # 1-5 stars
    comment = TextField()
    created_at = DateTimeField()
    
    # Use:
    # - Product reviews
    # - Ratings display
    # - Social proof
```

**Common Queries:**
```python
# Get item reviews
reviews = Review.objects.filter(item=item_id)

# Average rating
avg_rating = reviews.aggregate(
    Avg('rating')
)['rating__avg']

# User's reviews
my_reviews = Review.objects.filter(author=request.user)
```

#### 6. User Model (Django Built-in)
```python
# Extended with UserProfile (One-to-One)
from django.contrib.auth.models import User

# Properties:
user.username
user.email
user.first_name
user.last_name
user.password  # Hashed
user.is_staff
user.is_superuser
user.userprofile  # Custom profile

# Common methods:
user.set_password(password)
user.check_password(password)
user.save()
```

---

## 👀 Views & Logic

### View Types

#### Function-Based Views
```python
def home(request):
    """Homepage view"""
    featured_items = Item.objects.filter(
        status='available'
    ).order_by('-created_at')[:6]
    
    return render(request, 'store/home.html', {
        'featured_items': featured_items,
    })
```

#### Protected Views (Login Required)
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
    """User dashboard - requires login"""
    orders = Order.objects.filter(buyer=request.user)
    return render(request, 'store/dashboard.html', {
        'orders': orders,
    })
```

#### POST Request Handling
```python
def sell_item(request):
    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        
        Item.objects.create(
            seller=request.user,
            title=title,
            price=price,
            image=image,
        )
        return redirect('item_detail', item_id=item.id)
    
    # GET request - show form
    return render(request, 'store/sell_item.html')
```

### Common View Patterns

**Getting Objects:**
```python
# Get single object
item = Item.objects.get(id=item_id)
item = get_object_or_404(Item, id=item_id)  # Better - 404 if not found

# Filter multiple
items = Item.objects.filter(status='available')
items = Item.objects.all()

# With conditions
items = Item.objects.filter(
    status='available',
    price__lte=100
)
```

**Ordering:**
```python
# Recent first
items = Item.objects.order_by('-created_at')

# Price low to high
items = Item.objects.order_by('price')

# Multiple fields
items = Item.objects.order_by('category', '-price')
```

**Filtering:**
```python
# Exact match
Item.objects.filter(id=5)

# Contains (case-insensitive)
Item.objects.filter(title__icontains='jacket')

# Greater than
Item.objects.filter(price__gte=50)

# Less than
Item.objects.filter(price__lte=100)

# Range
Item.objects.filter(price__range=[20, 100])

# Date range
Item.objects.filter(created_at__date=today)
```

**Aggregations:**
```python
from django.db.models import Count, Avg, Sum

# Count
item_count = Item.objects.count()

# Average
avg_price = Item.objects.aggregate(Avg('price'))

# Sum
total_sales = Order.objects.aggregate(Sum('total_price'))

# Group by
from django.db.models import Count
items_per_category = Item.objects.values(
    'category'
).annotate(count=Count('id'))
```

---

## 🔗 URL Routing

### app urls.py Structure

```python
from django.urls import path
from . import views

urlpatterns = [
    # Home & browsing
    path('', views.home, name='home'),
    path('browse/', views.item_list, name='item_list'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Selling
    path('sell/', views.sell_item, name='sell_item'),
    path('item/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    
    # Buying
    path('item/<int:item_id>/buy/', views.buy_item, name='buy_item'),
    path('item/<int:item_id>/review/', views.add_review, name='add_review'),
    
    # User
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

### Reverse URLs in Templates

```html
<!-- Generate URLs dynamically -->
<a href="{% url 'home' %}">Home</a>
<a href="{% url 'item_detail' item.id %}">View Item</a>
<a href="{% url 'seller_profile' seller.id %}">Profile</a>

<!-- With query parameters -->
<a href="{% url 'item_list' %}?q=jacket">Search</a>
```

---

## 📄 Templates

### Template Hierarchy

```
base.html (Master template)
├── home.html
├── item_list.html
├── item_detail.html
├── dashboard.html
└── ... other templates
```

### Template Tags

**Template Variables:**
```html
<!-- Display data -->
{{ item.title }}
{{ item.price }}

<!-- Conditional -->
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}</p>
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}

<!-- Loops -->
{% for item in items %}
    <h3>{{ item.title }}</h3>
{% empty %}
    <p>No items found</p>
{% endfor %}

<!-- Filters -->
{{ date_value|date:"M d, Y" }}
{{ text|truncatewords:20 }}
{{ items|length }}
```

### Form Handling

**Simple Form:**
```html
<form method="post">
    {% csrf_token %}
    
    <label>Title</label>
    <input type="text" name="title" required>
    
    <label>Price</label>
    <input type="number" name="price" step="0.01" required>
    
    <button type="submit">Submit</button>
</form>
```

**Django Form (Better Practice):**
```python
from django import forms

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'category']
```

```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

---

## 🎨 Static Files

### Structure
```
store/static/
├── css/
│   └── style.css          # Main stylesheet
└── js/
    └── script.js          # JavaScript (optional)
```

### Using Static Files

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

### CSS Variables

```css
:root {
    --primary-dark: #1a2d4d;
    --secondary-pink: #ff3b81;
}

.button {
    background-color: var(--secondary-pink);
}
```

---

## 👨‍💼 Admin Interface

### Admin Setup (admin.py)

```python
from django.contrib import admin
from .models import Item, Category, Order

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'status')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
```

### Admin Features

**List View Options:**
```python
list_display = ()          # Columns shown
list_filter = ()           # Right sidebar filters
search_fields = ()         # Search bar
ordering = ()              # Default sorting
readonly_fields = ()       # Read-only fields
```

**Actions:**
```python
@admin.action(description="Mark as sold")
def mark_sold(modeladmin, request, queryset):
    queryset.update(status='sold')

actions = [mark_sold]
```

---

## 🛠️ Common Tasks

### Add a New Field to Model

```python
# 1. Add field to model
class Item(models.Model):
    new_field = models.CharField(max_length=100)

# 2. Create migration
python manage.py makemigrations

# 3. Apply migration
python manage.py migrate

# 4. Update admin if needed
list_display = (..., 'new_field')
```

### Add a New View

```python
# 1. Create view in views.py
def my_view(request):
    data = Model.objects.all()
    return render(request, 'template.html', {'data': data})

# 2. Add URL in urls.py
path('my-route/', views.my_view, name='my_view'),

# 3. Create template
# store/templates/store/template.html
```

### Query Database

```python
# Via Django shell
python manage.py shell

>>> from store.models import Item
>>> items = Item.objects.all()
>>> items.count()
>>> item = items.first()
>>> print(item.title)
```

### Reset Database

```bash
# Delete current database
del db.sqlite3

# Run migrations
python manage.py migrate

# Create new superuser
python manage.py createsuperuser

# Populate categories
python manage.py populate_categories
```

### Create Fixtures (Test Data)

```bash
# Dump data
python manage.py dumpdata store > data.json

# Load data
python manage.py loaddata data.json
```

---

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Use different port
python manage.py runserver 8001

# Or find what's using it (Windows)
netstat -ano | findstr :8000
```

**Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic

# Or in development, ensure DEBUG=True in settings
```

**Database Errors**
```bash
# Check migrations
python manage.py showmigrations

# Run migrations
python manage.py migrate

# Create missing tables
python manage.py migrate --run-syncdb
```

**Import Errors**
```bash
# Ensure app is in INSTALLED_APPS
# settings.py: INSTALLED_APPS = [..., 'store']

# Check Python path
python manage.py shell
import store
```

**Template Not Found**
```bash
# Check TEMPLATES setting
# Ensure templates/ folder exists
# Check for typos in render() call

python manage.py findstatic template_name.html
```

### Debug Mode

```python
# In settings.py
DEBUG = True  # Set to False in production

# View SQL queries
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    items = Item.objects.all()
    
print(context.captured_queries)
```

---

## 📊 Performance Tips

### Optimize Queries

```python
# Bad - N+1 query problem
items = Item.objects.all()
for item in items:
    print(item.seller.username)  # Extra query per item

# Good - Use select_related
items = Item.objects.select_related('seller')

# Or prefetch_related
items = Item.objects.prefetch_related('reviews')
```

### Use Pagination

```python
from django.core.paginator import Paginator

items = Item.objects.all()
paginator = Paginator(items, 20)  # 20 items per page
page = paginator.get_page(request.GET.get('page'))

# In template
{{ page.object_list }}
{{ page.has_next }}
{{ page.next_page_number }}
```

### Cache Results

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def category_items(request, category_id):
    ...
```

---

## 🧪 Testing

### Basic Test

```python
# store/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Item

class ItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test123'
        )
        self.item = Item.objects.create(
            seller=self.user,
            title='Test Item',
            price=50.00,
        )
    
    def test_item_creation(self):
        self.assertEqual(self.item.title, 'Test Item')
        self.assertEqual(self.item.price, 50.00)
    
    def test_item_list_view(self):
        client = Client()
        response = client.get('/browse/')
        self.assertEqual(response.status_code, 200)
```

**Run tests:**
```bash
python manage.py test
python manage.py test store.tests.ItemTestCase
```

---

## 📝 Logging

```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# In views.py
import logging
logger = logging.getLogger(__name__)

logger.info("User logged in")
logger.error("Error occurred")
```

---

## 🔐 Security Best Practices

### Input Validation

```python
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

# Validate in model
class Item(models.Model):
    website = URLField(validators=[URLValidator()])

# Validate in view
if not Item.objects.filter(id=item_id).exists():
    raise ValidationError("Item not found")
```

### CSRF Protection

```html
<!-- Always include in forms -->
<form method="post">
    {% csrf_token %}
    ...
</form>
```

### SQL Injection Prevention

```python
# Bad
Item.objects.raw("SELECT * FROM item WHERE id=" + str(id))

# Good
Item.objects.filter(id=id)
```

---

## 🚀 Deployment Preparation

### Create .env File

```bash
# .env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/db
```

### Update settings.py

```python
import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/stable/topics/http/views/)
- [Django Templates](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

---

## 💡 Tips & Tricks

### Quick Debug
```python
# Print queries in template
{% debug %}

# Check context
{{ request.user }}
{{ request.method }}
```

### Management Commands
```bash
# Create custom command
# store/management/commands/mycmd.py

# Run it
python manage.py mycmd

# With arguments
python manage.py mycmd --argument=value
```

### Fixtures
```bash
# Create
python manage.py dumpdata store > backup.json

# Load
python manage.py loaddata backup.json
```

---

**Happy Coding! 🚀**

For questions, refer to Django documentation or review the code comments throughout this project.
