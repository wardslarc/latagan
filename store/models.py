from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class Category(models.Model):
    """Product category model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(models.Model):
    """Thrift item listing model"""
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items_for_sale')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    image = models.ImageField(upload_to='items/')
    condition = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('like_new', 'Like New'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('poor', 'Poor'),
        ],
        default='good'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """Extended user profile for sellers"""
    MODE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_seller = models.BooleanField(default=True)
    current_mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='buyer')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Order(models.Model):
    """Purchase order model"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.item.title}"


class Review(models.Model):
    """Product review model"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.author.username} - {self.item.title}"


class Cart(models.Model):
    """Shopping cart for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total(self):
        """Calculate cart total"""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_item_count(self):
        """Get total items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Individual item in a cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'item')

    def __str__(self):
        return f"{self.item.title} x{self.quantity}"

    def get_subtotal(self):
        """Calculate subtotal for this cart item"""
        return self.item.price * self.quantity


class Message(models.Model):
    """Messages between users about items"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} about {self.item.title}"
