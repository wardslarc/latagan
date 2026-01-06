from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Item, Category, UserProfile, Order, Review, Cart, CartItem, Message
from django.db.models import Q, Avg as models_Avg
from django.db import models
from django.contrib import messages


def home(request):
    """Home page - featured items"""
    featured_items = Item.objects.filter(status='available').order_by('-created_at')
    
    # Exclude items already in user's cart if authenticated
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item_ids = cart.items.values_list('item_id', flat=True)
            featured_items = featured_items.exclude(id__in=cart_item_ids)
        except Cart.DoesNotExist:
            pass
    
    # Apply slice after filtering
    featured_items = featured_items[:6]
    
    categories = Category.objects.all()
    context = {
        'featured_items': featured_items,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def item_list(request):
    """Browse all items with search and filter"""
    items = Item.objects.filter(status='available')
    categories = Category.objects.all()
    
    # Search
    query = request.GET.get('q', '')
    if query:
        items = items.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Filter by category
    category_id = request.GET.get('category', '')
    if category_id:
        items = items.filter(category_id=category_id)
    
    # Filter by price
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        items = items.filter(price__gte=min_price)
    if max_price:
        items = items.filter(price__lte=max_price)
    
    # Filter by condition
    condition = request.GET.get('condition', '')
    if condition:
        items = items.filter(condition=condition)
    
    context = {
        'items': items,
        'categories': categories,
        'query': query,
    }
    return render(request, 'store/item_list.html', context)


def item_detail(request, item_id):
    """Single item detail page"""
    item = get_object_or_404(Item, id=item_id)
    reviews = item.reviews.all()
    seller_profile = item.seller.userprofile
    
    # Check if user has purchased this item
    has_purchased = False
    has_in_cart = False
    if request.user.is_authenticated:
        has_purchased = Order.objects.filter(
            item=item,
            buyer=request.user
        ).exists()
        # Check if item is in user's cart
        user_cart = Cart.objects.filter(user=request.user).first()
        if user_cart:
            has_in_cart = CartItem.objects.filter(
                cart=user_cart,
                item=item
            ).exists()
    
    context = {
        'item': item,
        'reviews': reviews,
        'seller_profile': seller_profile,
        'has_purchased': has_purchased,
        'has_in_cart': has_in_cart,
    }
    return render(request, 'store/item_detail.html', context)


def category_items(request, category_id):
    """Items by category"""
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(status='available', category=category)
    categories = Category.objects.all()
    
    context = {
        'category': category,
        'items': items,
        'categories': categories,
    }
    return render(request, 'store/category_items.html', context)


def seller_profile(request, seller_id):
    """Seller profile page"""
    seller = get_object_or_404(User, id=seller_id)
    seller_profile = get_object_or_404(UserProfile, user=seller)
    items = Item.objects.filter(seller=seller, status='available')
    
    context = {
        'seller': seller,
        'seller_profile': seller_profile,
        'items': items,
    }
    return render(request, 'store/seller_profile.html', context)


def register(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'store/register.html')


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'store/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    """User dashboard - selling and purchase history"""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    my_items = Item.objects.filter(seller=request.user)
    my_orders = Order.objects.filter(buyer=request.user)
    
    context = {
        'user_profile': user_profile,
        'my_items': my_items,
        'my_orders': my_orders,
    }
    return render(request, 'store/dashboard.html', context)


@login_required(login_url='login')
@login_required(login_url='login')
def sell_item(request):
    """Create a new item listing"""
    categories = Category.objects.all()
    user_profile = request.user.userprofile
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        condition = request.POST.get('condition')
        image = request.FILES.get('image')
        
        # Check if user has enough credits
        if user_profile.credits < 10:
            messages.error(request, f'You need at least 10 credits to post an item. You have {user_profile.credits} credits.')
            return redirect('sell_item')
        
        category = get_object_or_404(Category, id=category_id)
        
        item = Item.objects.create(
            seller=request.user,
            title=title,
            description=description,
            price=price,
            category=category,
            condition=condition,
            image=image,
        )
        
        # Deduct 10 credits for posting
        user_profile.credits -= 10
        user_profile.save()
        
        messages.success(request, f'Item listed successfully! {user_profile.credits} credits remaining.')
        return redirect('item_detail', item_id=item.id)
    
    context = {'categories': categories, 'user_credits': user_profile.credits}
    return render(request, 'store/sell_item.html', context)


@login_required(login_url='login')
def buy_item(request, item_id):
    """Purchase an item"""
    item = get_object_or_404(Item, id=item_id)
    
    if request.user == item.seller:
        messages.error(request, 'You cannot buy your own items')
        return redirect('item_detail', item_id=item.id)
    
    if request.method == 'POST':
        order = Order.objects.create(
            item=item,
            buyer=request.user,
            total_price=item.price,
        )
        
        item.status = 'sold'
        item.save()
        
        messages.success(request, 'Purchase successful! Check your dashboard for details.')
        return redirect('dashboard')
    
    context = {'item': item}
    return render(request, 'store/buy_item.html', context)


@login_required(login_url='login')
@require_POST
def add_review(request, item_id):
    """Add review to an item"""
    item = get_object_or_404(Item, id=item_id)
    
    # Check if user purchased this item
    if not Order.objects.filter(item=item, buyer=request.user).exists():
        return JsonResponse({'error': 'You must purchase the item to review it'}, status=403)
    
    rating = request.POST.get('rating')
    comment = request.POST.get('comment')
    
    review = Review.objects.create(
        item=item,
        author=request.user,
        rating=rating,
        comment=comment,
    )
    
    return JsonResponse({'success': True, 'message': 'Review added successfully'})


@login_required(login_url='login')
def edit_item(request, item_id):
    """Edit item listing"""
    item = get_object_or_404(Item, id=item_id)
    categories = Category.objects.all()
    
    if request.user != item.seller:
        messages.error(request, 'You do not have permission to edit this item')
        return redirect('item_detail', item_id=item.id)
    
    if request.method == 'POST':
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.price = request.POST.get('price')
        item.category_id = request.POST.get('category')
        item.condition = request.POST.get('condition')
        if request.FILES.get('image'):
            item.image = request.FILES.get('image')
        item.save()
        
        messages.success(request, 'Item updated successfully!')
        return redirect('item_detail', item_id=item.id)
    
    context = {
        'item': item,
        'categories': categories,
    }
    return render(request, 'store/edit_item.html', context)


@login_required(login_url='login')
def view_cart(request):
    """View shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
@require_POST
def add_to_cart(request, item_id):
    """Add item to cart (AJAX)"""
    item = get_object_or_404(Item, id=item_id)
    
    if item.seller == request.user:
        return JsonResponse({'error': 'You cannot add your own items to cart'}, status=400)
    
    if item.status != 'available':
        return JsonResponse({'error': 'This item is not available'}, status=400)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return JsonResponse({
        'success': True,
        'message': f'{item.title} added to cart',
        'cart_count': cart.get_item_count(),
    })


@login_required(login_url='login')
@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    item = get_object_or_404(Item, id=item_id)
    cart = get_object_or_404(Cart, user=request.user)
    
    CartItem.objects.filter(cart=cart, item=item).delete()
    
    return redirect('view_cart')


@login_required(login_url='login')
@require_POST
def update_cart_quantity(request, item_id):
    """Update item quantity in cart (AJAX)"""
    item = get_object_or_404(Item, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item=item)
    
    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    return JsonResponse({
        'success': True,
        'cart_total': float(cart.get_total()),
        'cart_count': cart.get_item_count(),
    })


@login_required(login_url='login')
def checkout(request):
    """Checkout and convert cart to orders"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('view_cart')
    
    if request.method == 'POST':
        # Create orders for each item in cart
        for cart_item in cart_items:
            order = Order.objects.create(
                item=cart_item.item,
                buyer=request.user,
                total_price=cart_item.get_subtotal(),
            )
            
            # Mark item as sold
            cart_item.item.status = 'sold'
            cart_item.item.save()
            
            # Remove from cart
            cart_item.delete()
        
        messages.success(request, 'Purchase completed successfully!')
        return redirect('dashboard')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)


@login_required(login_url='login')
@login_required(login_url='login')
def user_profile(request):
    """User profile page"""
    user_profile = UserProfile.objects.get(user=request.user)
    items_count = Item.objects.filter(seller=request.user, status='available').count()
    purchases_count = Order.objects.filter(buyer=request.user).count()
    reviews_count = Review.objects.filter(author=request.user).count()
    
    # Calculate average rating from reviews authored by user
    reviews = Review.objects.filter(author=request.user)
    if reviews.exists():
        avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
    else:
        avg_rating = None
    
    context = {
        'user_profile': user_profile,
        'items_count': items_count,
        'purchases_count': purchases_count,
        'reviews_count': reviews_count,
        'avg_rating': avg_rating,
    }
    return render(request, 'store/profile.html', context)


@login_required(login_url='login')
def toggle_user_mode(request):
    """Toggle between buyer and seller mode"""
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        # Toggle mode
        if user_profile.current_mode == 'buyer':
            user_profile.current_mode = 'seller'
        else:
            user_profile.current_mode = 'buyer'
        user_profile.save()
        messages.success(request, f'Switched to {user_profile.current_mode.title()} mode')
        return redirect('profile')
    return redirect('profile')
@login_required(login_url='login')
def item_chat(request, item_id):
    """Chat about a specific item"""
    item = get_object_or_404(Item, id=item_id)
    
    # Check if user has added this item to cart
    try:
        cart = Cart.objects.get(user=request.user)
        has_item_in_cart = cart.items.filter(item=item).exists()
    except Cart.DoesNotExist:
        has_item_in_cart = False
    
    if not has_item_in_cart:
        messages.error(request, 'You must add this item to your cart to chat about it')
        return redirect('item_detail', item_id=item.id)
    
    # Get all messages for this item with current user
    all_messages = Message.objects.filter(item=item).filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by('created_at')
    
    # Mark received messages as read
    Message.objects.filter(item=item, recipient=request.user, is_read=False).update(is_read=True)
    
    # Get the other user (seller or buyer)
    other_user = item.seller if item.seller != request.user else None
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content and other_user:
            Message.objects.create(
                item=item,
                sender=request.user,
                recipient=other_user,
                content=content,
            )
            return redirect('item_chat', item_id=item.id)
    
    context = {
        'item': item,
        'messages': all_messages,
        'other_user': other_user,
        'has_item_in_cart': has_item_in_cart,
    }
    return render(request, 'store/item_chat.html', context)


@login_required(login_url='login')
@login_required
def messages_inbox(request):
    """View all message conversations"""
    # Get all unique items the user is chatting about
    items_with_messages = Item.objects.filter(
        Q(messages__sender=request.user) | Q(messages__recipient=request.user)
    ).distinct().prefetch_related('messages')
    
    # Build conversation data
    conversations = []
    for item in items_with_messages:
        # Get messages for this item with this user
        messages = Message.objects.filter(item=item).filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).order_by('created_at')
        
        if messages.exists():
            # Get the other user in conversation
            last_message = messages.last()
            other_user = last_message.sender if last_message.recipient == request.user else last_message.recipient
            
            # Count unread messages for this item
            unread_count = messages.filter(
                recipient=request.user,
                is_read=False
            ).count()
            
            conversations.append({
                'item': item,
                'other_user': other_user,
                'last_message': last_message,
                'unread_count': unread_count,
                'messages': messages,
            })
    
    # Sort by last message date (newest first)
    conversations.sort(key=lambda x: x['last_message'].created_at, reverse=True)
    
    # Count total unread messages
    unread_count = Message.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    context = {
        'items_with_messages': conversations,
        'unread_count': unread_count,
    }
    return render(request, 'store/messages_inbox.html', context)


@login_required(login_url='login')
def add_credits(request):
    """Add credits to user account"""
    user_profile = request.user.userprofile
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        
        try:
            amount = int(amount)
            if amount < 10:
                messages.error(request, 'Minimum credit purchase is 10 credits.')
                return redirect('add_credits')
            
            # Add credits to profile
            user_profile.credits += amount
            user_profile.save()
            
            messages.success(request, f'Successfully added {amount} credits! Total: {user_profile.credits} credits')
            return redirect('profile')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid credit amount.')
            return redirect('add_credits')
    
    credit_packages = [
        {'credits': 10, 'price': '$0.99'},
        {'credits': 50, 'price': '$4.99'},
        {'credits': 100, 'price': '$9.99'},
        {'credits': 250, 'price': '$24.99'},
        {'credits': 500, 'price': '$49.99'},
    ]
    
    context = {
        'user_credits': user_profile.credits,
        'credit_packages': credit_packages,
    }
    return render(request, 'store/add_credits.html', context)
