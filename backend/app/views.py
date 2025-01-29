from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Cart
from django.db.models import Sum, F
from django.contrib import messages



@login_required
def home(request):
    category = request.GET.get('category', None)  
    sort_by_price = request.GET.get('sort', None)

    products = Product.objects.all()

    # Apply category filtering
    if category:
        products = products.filter(product_category=category)  # Updated field name

    # Apply sorting if specified
    if sort_by_price == 'low_to_high':
        products = products.order_by('product_price')
    elif sort_by_price == 'high_to_low':
        products = products.order_by('-product_price')

    # Add cart information for authenticated users
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_product_ids = {item.product_id: item.quantity for item in cart_items}
        cart_count = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    else:
        cart_product_ids = {}
        cart_count = 0

    # Annotate products with cart quantity
    for product in products:
        product.in_cart = cart_product_ids.get(product.product_id, 0)

    return render(request, 'app/home.html', {'products': products, 'cart_count': cart_count})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

# Update Cart Quantity
@login_required
def update_cart(request, product_id, action):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif action == 'decrement' and cart_item.quantity == 1:
        cart_item.delete()
        return redirect('home')
    cart_item.save()
    return redirect('home')

# Remove from Cart
@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('home')


# Update Cart Quantity
@login_required
def cartpage_update_cart(request, product_id, action):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif action == 'decrement' and cart_item.quantity == 1:
        cart_item.delete()
        return redirect('cart')
    cart_item.save()
    return redirect('cart')

# Remove from Cart
@login_required
def cartpage_remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('cart')


@login_required
def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            item.subtotal = item.quantity * item.product.product_price
        total = sum(item.subtotal for item in cart_items)  
        cart_count = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    else:
        cart_items = []
        total = 0
        cart_count = 0
    return render(request, 'app/cart.html', {'cart_items': cart_items, 'total': total, 'cart_count':cart_count })

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) 
            return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'app/signin.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data.get('username')
            messages.success(request,f'welcome{ username }, your account is created!!!')
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

@login_required
def payment(request):
    if request.method == "POST":
    
        errors = {}
        card_number = request.POST.get("cardNumber")
        card_expiry = request.POST.get("cardExpiry")
        card_cvv = request.POST.get("cardCVV")
        cardholder_name = request.POST.get("cardholderName")

        if not card_number or len(card_number) != 16 or not card_number.isdigit():
            errors["cardNumber"] = "Invalid card number. Must be 16 digits."

        if not card_expiry or len(card_expiry) != 5 or "/" not in card_expiry:
            errors["cardExpiry"] = "Invalid expiry date. Must be in MM/YY format."

        if not card_cvv or len(card_cvv) != 3 or not card_cvv.isdigit():
            errors["cardCVV"] = "Invalid CVV. Must be 3 digits."

        if not cardholder_name or len(cardholder_name.strip()) == 0:
            errors["cardholderName"] = "Cardholder name cannot be empty."

        if errors:
            return render(request, 'app/payment.html', {"errors": errors, "form_data": request.POST})

        if request.user.is_authenticated:
            Cart.objects.filter(user=request.user).delete()

        Cart.objects.filter(user=request.user).delete()
        return redirect('thank_you')

    return render(request, 'app/payment.html')

@login_required
def thank_you(request):
    return render(request, 'app/thank_you.html')

from django.shortcuts import redirect

def redirect_to_signin(request):
    # If the user is authenticated, redirect them to the home page
    if request.user.is_authenticated:
        return redirect('home') 
    else:
        return redirect('signin')  


def address(request):
    return render(request,'app/address.html')