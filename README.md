# Latagan - Online Thrift Store

A beautiful Django-based online thrift store where users can buy and sell unique secondhand items.

## Features

- **User Authentication**: Register, login, and manage user profiles
- **Item Listings**: Sellers can create, edit, and manage their item listings
- **Browse & Search**: Users can browse items with filters (category, condition, price)
- **Purchase System**: Complete buy/sell workflow with order tracking
- **Seller Profiles**: View seller information and their available items
- **Reviews**: Customers can leave reviews on purchased items
- **Dashboard**: Personalized dashboard to manage items and purchases
- **Responsive Design**: Mobile-friendly interface with modern styling

## Color Scheme

Inspired by ResiMax design:
- **Primary Dark**: #1a2d4d (Dark navy blue)
- **Secondary Pink**: #ff3b81 (Vibrant pink)
- **Accent Purple**: #8b5cf6 (Purple accent)
- **Light Gray**: #f5f5f5 (Background)

## Installation

### 1. Clone/Download the Project

```bash
cd latagan
```

### 2. Create a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database

```bash
python manage.py migrate
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
latagan/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database
│
├── latagan_project/                   # Main project configuration
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # URL routing
│   └── wsgi.py                        # WSGI configuration
│
└── store/                             # Main Django app
    ├── migrations/                    # Database migrations
    ├── static/
    │   └── css/
    │       └── style.css              # Main stylesheet
    ├── templates/
    │   ├── base.html                  # Base template
    │   └── store/
    │       ├── home.html              # Home page
    │       ├── item_list.html         # Browse items
    │       ├── item_detail.html       # Item detail page
    │       ├── category_items.html    # Category view
    │       ├── seller_profile.html    # Seller profile
    │       ├── register.html          # Registration
    │       ├── login.html             # Login
    │       ├── dashboard.html         # User dashboard
    │       ├── sell_item.html         # Create listing
    │       ├── edit_item.html         # Edit listing
    │       └── buy_item.html          # Confirm purchase
    ├── admin.py                       # Django admin configuration
    ├── apps.py                        # App configuration
    ├── models.py                      # Database models
    ├── urls.py                        # App URL routing
    ├── views.py                       # View logic
    └── tests.py                       # Tests
```

## Database Models

### User-Related Models
- **UserProfile**: Extended user information (bio, rating, phone, address)

### Product Models
- **Category**: Product categories
- **Item**: Product listings with details, pricing, and status
- **Review**: Customer reviews for items

### Transaction Models
- **Order**: Purchase records

## URL Routes

| URL | Purpose |
|-----|---------|
| `/` | Home page |
| `/browse/` | Browse all items |
| `/item/<id>/` | Item detail page |
| `/category/<id>/` | Items by category |
| `/seller/<id>/` | Seller profile |
| `/register/` | User registration |
| `/login/` | User login |
| `/logout/` | User logout |
| `/dashboard/` | User dashboard |
| `/sell/` | Create new listing |
| `/item/<id>/edit/` | Edit listing |
| `/item/<id>/buy/` | Purchase item |
| `/item/<id>/review/` | Add review |
| `/admin/` | Django admin panel |

## Usage

### As a Buyer
1. Browse items on the home page or use the search
2. Filter by category, condition, and price
3. View item details and seller information
4. Register or login to make a purchase
5. Complete the purchase and leave a review

### As a Seller
1. Register for an account
2. Go to Dashboard > List New Item
3. Fill in item details (title, description, price, condition, image)
4. View your listings and sales in the dashboard
5. Edit or remove listings as needed

## Customization

### Adding More Categories

Use the Django admin panel:
1. Go to `/admin/`
2. Login with your superuser credentials
3. Click on "Categories"
4. Click "Add Category"

### Modifying Styles

Edit `store/static/css/style.css` to customize:
- Colors (update CSS variables in `:root`)
- Fonts and typography
- Layout and spacing
- Component styling

### Extending Features

Possible enhancements:
- Payment gateway integration (Stripe, PayPal)
- Email notifications
- Wishlist/favorites feature
- Advanced search with filters
- User ratings system
- Messaging between buyers and sellers
- Image gallery with multiple photos
- Shipping integration

## Admin Panel

Access Django admin at `/admin/`:
- Manage products, categories, users
- View and process orders
- Moderate reviews
- Track seller information

## Security Notes

⚠️ **For Production:**
- Change `SECRET_KEY` in settings.py
- Set `DEBUG = False`
- Configure allowed hosts
- Use environment variables for sensitive data
- Set up proper database (PostgreSQL recommended)
- Use HTTPS
- Configure CSRF and security headers

## License

This project is open source. Feel free to use and modify!

## Support

For issues or questions, please refer to Django documentation:
- https://docs.djangoproject.com/

---

**Made with ❤️ for thrift lovers**
