from django.shortcuts import render, redirect
from .models import Product, Order

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def dashboard(request):

    return render(request, 'home.html')

def home(request):

    products = Product.objects.all()

    return render(request, 'index.html', {
        'products': products
    })


def add_to_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('/cart/')


def remove_from_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('/cart/')


def cart(request):

    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def product_detail(request, product_id):

    product = Product.objects.get(id=product_id)

    return render(request, 'product_detail.html', {
        'product': product
    })


def register_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # ✅ CHECK IF USER EXISTS
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists. Please choose another one.'
            })

        # create user safely
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        return redirect('/login/')

    return render(request, 'register.html')

def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/home/')

        else:

            return render(request, 'login.html', {
                'error': 'Invalid Username or Password'
            })

    return render(request, 'login.html')


def logout_user(request):

    logout(request)

    return redirect('/home/')


def checkout(request):

    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':

        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']

        Order.objects.create(
            customer_name=name,
            address=address,
            phone=phone
        )

        request.session['cart'] = {}

        return render(request, 'success.html', {
            'total': total
        })

    return render(request, 'checkout.html', {
        'total': total,
        'cart_items': cart_items
    })
def payment(request):

    return render(request, 'checkout.html')