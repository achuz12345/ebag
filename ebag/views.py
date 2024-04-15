from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CartItem, Product
from .forms import ProductForm
from django.contrib.auth.models import User


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_superuser:
                return redirect("home")
            return redirect('index')
          # Redirect to index upon successful login
        else:
            messages.error(request, 'Username or Password is incorrect.')
    
    return render(request, 'login.html')


# User Register


from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileInfoForm
from django.contrib import messages

def register_request(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            return redirect('login')
        else:
            messages.error(request, 'Username or Password is incorrect.')
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


# User Logout
@login_required
def logout_view(request):
  logout(request)
  return redirect('login')

# Home Page
@login_required
def home(request):
  products = Product.objects.all()
  return render(request, 'home.html', {'products': products})

# Add Product

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# Edit Product
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})


# Delete Product
@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('home')
    return render(request, 'delete_product.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_list(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'product_list.html', {'products': products})

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
 
@login_required
def add_to_cart(request, product_id): 
    product = Product.objects.get(id=product_id) 
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id) 
        if product.quantity > 0: 
            cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user) 
            cart_item.quantity += 1 
            cart_item.save()
        else:
            messages.error(request, 'Product is not available at the moment.')
        return redirect('view_cart')
    else:
        messages.error(request, 'Please log in to add items to your cart.')
        return redirect('login')
 
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product = cart_item.product
    product.quantity += cart_item.quantity
    product.save()
    if cart_item.quantity == 1: # check if the quantity is 1, not 0
        cart_item.delete()
    else:
        cart_item.quantity -= 1 # decrease the quantity by 1
        cart_item.save()

    return redirect('view_cart')

def product_list(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.filter(name__icontains=query)
    
    return render(request, 'product_list.html', {'products': products, 'query': query, 'category': category})


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem
from .forms import CheckoutForm

@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST, request=request)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.shipping_address = form.cleaned_data['shipping_address']
            user.contact_info = form.cleaned_data['contact_info']
            user.save()

            cart_items = CartItem.objects.filter(user=user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)

            return render(request, 'purchase_confirmation.html', {'user': user, 'cart_items': cart_items, 'total_price': total_price})
    else:
        form = CheckoutForm(request=request)
    return render(request, 'checkout.html', {'form': form})

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import PenCategory

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        new_category = PenCategory(name=name)
        new_category.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'add_category.html')
from django.shortcuts import render, redirect
from .models import CartItem, Product
from django.contrib import messages

def confirm_purchase(request):
    # Get the user's cart items
    cart_items = CartItem.objects.filter(user=request.user)

    # Update product quantities and remove items from the cart
    for item in cart_items:
        product = item.product
        if product.quantity >= item.quantity:
            product.quantity -= item.quantity
            product.save()
        else:
            # If the product quantity is not sufficient, handle accordingly
            messages.warning(request, f"Product {product.name} is not available in sufficient quantity.")

        # Remove the item from the cart
        item.delete()

    return redirect('thank_you_page')
def thank_you_page(request):
    return render(request, 'thank_you.html')
def product_detail(request, product_id): 
    product = Product.objects.get(id=product_id) 
    return render(request, 'product_detail.html', {'product': product})

def index_home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def first(request):
    products = Product.objects.all()
    return render(request, 'first.html', {'products': products})

def index_home(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'index.html', {'products': products})

def index_home(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.filter(name__icontains=query)
    
    return render(request, 'index.html', {'products': products, 'query': query, 'category': category})

def first(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'first.html', {'products': products})