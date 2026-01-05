from django.contrib import admin
from .models import Category, Item, UserProfile, Order, Review

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'status', 'condition', 'created_at')
    list_filter = ('status', 'condition', 'category', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_seller', 'rating', 'created_at')
    list_filter = ('is_seller', 'created_at')
    search_fields = ('user__username', 'user__email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'buyer', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('item__title', 'buyer__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('item__title', 'author__username')
