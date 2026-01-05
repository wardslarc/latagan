from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('browse/', views.item_list, name='item_list'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('category/<int:category_id>/', views.category_items, name='category_items'),
    path('seller/<int:seller_id>/', views.seller_profile, name='seller_profile'),
    
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/toggle-mode/', views.toggle_user_mode, name='toggle_user_mode'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/preferences/', views.preferences, name='preferences'),
    
    # Dashboard & Selling
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sell/', views.sell_item, name='sell_item'),
    path('item/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    
    # Buying & Reviews
    path('item/<int:item_id>/buy/', views.buy_item, name='buy_item'),
    path('item/<int:item_id>/review/', views.add_review, name='add_review'),
    
    # Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Messaging
    path('item/<int:item_id>/chat/', views.item_chat, name='item_chat'),
    path('messages/', views.messages_inbox, name='messages_inbox'),
    
    # Credits
    path('credits/add/', views.add_credits, name='add_credits'),
]
