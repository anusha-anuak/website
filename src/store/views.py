from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Cart, CartItem, Order, OrderItem

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.get('cart_session')
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
            request.session['cart_session'] = session_id
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(stock__gt=0)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, f"{product.name} added to cart.")
    return redirect('cart_detail')

def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})

def remove_from_cart(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')

    messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')

from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm, UserUpdateForm

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    # Also fetch user's orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'store/profile.html', {'form': form, 'orders': orders})

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' created successfully!")
            return redirect('product_detail', slug=product.slug)
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

@user_passes_test(is_staff)
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect('product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})

@user_passes_test(is_staff)
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('product_list')
    return render(request, 'store/delete_product.html', {'product': product})

@user_passes_test(is_staff)
def manage_products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'store/manage_products.html', {'products': products})

@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart.items.exists():
        return redirect('product_list')
        
    if request.method == 'POST':
        # Save shipping info to session
        request.session['shipping_info'] = {
            'full_name': request.POST.get('full_name'),
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'postal_code': request.POST.get('postal_code'),
        }
        return redirect('payment')
        
    return render(request, 'store/checkout.html', {'cart': cart})

@login_required
def payment(request):
    cart = get_cart(request)
    if not cart.items.exists():
        return redirect('product_list')
    
    shipping_info = request.session.get('shipping_info')
    if not shipping_info:
        messages.error(request, "Please provide shipping information first.")
        return redirect('checkout')

    if request.method == 'POST':
        # Simulate payment processing (always successful for now)
        
        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=shipping_info['full_name'],
            address=shipping_info['address'],
            city=shipping_info['city'],
            postal_code=shipping_info['postal_code'],
            total_price=cart.total_price
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            
        # Clear cart and session
        cart.items.all().delete()
        if 'shipping_info' in request.session:
            del request.session['shipping_info']
        
        messages.success(request, "Payment successful! Order placed.")
        return redirect('order_history')

    return render(request, 'store/payment.html', {'cart': cart, 'shipping_info': shipping_info})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})
