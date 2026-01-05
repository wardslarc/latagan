# Latagan - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Run Setup Script

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Create Sample Categories

After setup completes, run:
```bash
python manage.py populate_categories
```

### Step 3: Start the Server

```bash
python manage.py runserver
```

### Step 4: Visit the Website

- **Main Site:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 📝 Creating Test Data

### 1. Access Admin Panel
- Go to http://127.0.0.1:8000/admin/
- Login with your superuser credentials

### 2. Add Sample Items
- Click on "Items"
- Click "Add Item"
- Fill in the details:
  - **Title:** Example product name
  - **Description:** Item details
  - **Price:** Amount in dollars
  - **Category:** Select from dropdown
  - **Condition:** Choose condition level
  - **Image:** Upload an image file

---

## 🎨 Color Scheme Reference

### Primary Colors
- **Dark Navy:** `#1a2d4d` - Main background
- **Pink:** `#ff3b81` - Accent color (buttons, highlights)
- **Purple:** `#8b5cf6` - Secondary accents
- **Light Gray:** `#f5f5f5` - Content background

### How Colors Are Used
```
Header/Nav:      Dark Navy with Pink accents
Buttons:         Gradient Pink to Dark Pink
Cards:           Light Gray with Dark Text
Highlights:      Pink (#ff3b81)
Text:            Dark Gray (#333) on light backgrounds
```

---

## 🗂️ Site Structure

### Navigation Flow

```
Home (/)
├── Browse (/browse/)
├── Item Detail (/item/<id>/)
├── Seller Profile (/seller/<id>/)
├── Category (/category/<id>/)
└── User Account
    ├── Login
    ├── Register
    ├── Dashboard (/dashboard/)
    │   ├── My Listings
    │   ├── My Purchases
    │   └── Profile
    └── Sell Item (/sell/)
```

---

## 👥 User Roles

### Buyers
- Browse items
- Search and filter products
- View item details
- Purchase items
- Leave reviews

### Sellers
- List items for sale
- Edit existing listings
- View purchase orders
- Manage inventory
- Receive ratings from buyers

---

## 📱 Responsive Design

The site is fully responsive and works on:
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

---

## 🔧 Customization Tips

### Change Colors
Edit `store/static/css/style.css`:
```css
:root {
    --primary-dark: #1a2d4d;      /* Change this */
    --secondary-pink: #ff3b81;    /* Change this */
    --accent-purple: #8b5cf6;     /* Change this */
    /* ... */
}
```

### Change Site Name
Edit `store/templates/base.html`:
```html
<a href="{% url 'home' %}" class="navbar-brand">
    🛍️ Latagan  <!-- Change text here -->
</a>
```

### Add More Categories
1. Go to Admin Panel
2. Click Categories
3. Click "Add Category"
4. Enter name and description

### Modify Item Fields
Edit `store/models.py` and add new fields to `Item` model, then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Issues
```bash
python manage.py migrate --run-syncdb
```

### Reset Database
```bash
del db.sqlite3  # Windows
rm db.sqlite3   # macOS/Linux
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_categories
```

---

## 📚 Key Features Explained

### Search & Filter
Located on `/browse/` page:
- **Search:** Find items by title or description
- **Category:** Filter by product type
- **Condition:** New, Like New, Good, Fair, Poor
- **Price Range:** Set min and max prices

### Dashboard
User's personal control center:
- **Your Listings:** Manage items you're selling
- **Your Purchases:** Track bought items
- **Profile:** View and edit account info

### Reviews System
- Only buyers can review items
- 5-star rating system
- Text comments
- Displayed on item detail page

### Order Management
**As Seller:**
- See incoming orders in admin panel
- Update order status (Pending → Confirmed → Shipped → Delivered)

**As Buyer:**
- Track purchase status in dashboard
- View order history and details

---

## 🔐 Security Notes for Production

Before going live:

1. **SECRET_KEY** - Generate a new one
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

2. **DEBUG** - Set to False
   ```python
   DEBUG = False
   ```

3. **ALLOWED_HOSTS** - Add your domain
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

4. **Database** - Use PostgreSQL instead of SQLite
   ```bash
   pip install psycopg2-binary
   ```

5. **Use HTTPS** - Configure SSL certificates

6. **Environment Variables** - Store secrets in .env file

---

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Templates](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Django Views](https://docs.djangoproject.com/en/stable/topics/http/views/)

---

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `manage.py` | Django command-line utility |
| `requirements.txt` | Python package dependencies |
| `store/models.py` | Database schema definitions |
| `store/views.py` | Business logic and request handlers |
| `store/urls.py` | URL routing configuration |
| `store/admin.py` | Django admin customization |
| `store/static/css/style.css` | Website styling |
| `store/templates/` | HTML templates |

---

## 🚀 Next Steps

1. ✅ Run setup script
2. ✅ Create superuser account
3. ✅ Populate categories
4. ✅ Create test items via admin panel
5. ✅ Register test user accounts
6. ✅ Test buying/selling flow
7. ✅ Customize colors and content
8. ✅ Deploy to production

---

## ❓ Support

For issues or questions:
- Check Django documentation
- Review code comments
- Check admin panel for data issues
- Look at browser console for JavaScript errors

---

**Happy Thrifting! 🛍️**
