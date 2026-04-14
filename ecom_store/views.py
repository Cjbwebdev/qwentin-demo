from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Product


def home(request):
    featured_products = Product.objects.filter(featured=True)[:8]
    categories = Category.objects.all()
    latest_items = Product.objects.filter(featured=True)[:6]
    return render(request, 'pages/home.html', {
        'featured_products': featured_products,
        'categories': categories,
        'latest_items': latest_items,
    })


def product_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        products = products.filter(category__slug=category_slug)
    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4] if product.category else Product.objects.filter(featured=True).exclude(pk=product.pk)[:4]
    return render(request, 'pages/detail.html', {
        'product': product,
        'related_items': related_products,
    })


def account(request):
    return render(request, 'pages/account.html', {
        'user': request.user,
        'orders': [],
    })


def _load_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def _build_cart(cart_data):
    items = []
    subtotal = Decimal('0.00')

    for product_id, quantity in cart_data.items():
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            continue
        qty = int(quantity)
        total_price = product.price * qty
        subtotal += total_price
        items.append({
            'id': product_id,
            'quantity': qty,
            'product': product,
            'total_price': f'${total_price:,.2f}',
        })

    total = subtotal
    return {
        'items': items,
        'subtotal': f'${subtotal:,.2f}',
        'shipping': 'Free',
        'total': f'${total:,.2f}',
    }


def cart_view(request):
    cart = _build_cart(_load_cart(request))
    return render(request, 'cart.html', {'cart': cart})


def cart_add(request):
    if request.method != 'POST':
        return redirect('product_list')

    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))
    cart = _load_cart(request)
    cart[str(product.pk)] = cart.get(str(product.pk), 0) + quantity
    _save_cart(request, cart)
    return redirect('cart')


def cart_update(request):
    if request.method != 'POST':
        return redirect('cart')

    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    cart = _load_cart(request)
    if item_id in cart:
        if action == 'increase':
            cart[item_id] += 1
        elif action == 'decrease':
            cart[item_id] = max(cart[item_id] - 1, 1)
        if cart[item_id] <= 0:
            cart.pop(item_id, None)
    _save_cart(request, cart)
    return redirect('cart')


def checkout_view(request):
    cart = _build_cart(_load_cart(request))
    return render(request, 'checkout.html', {'cart': cart})


def checkout_complete(request):
    if request.method == 'POST':
        request.session['cart'] = {}
        request.session.modified = True
        return redirect('home')
    return redirect('checkout')


def category_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.all()
    current_category = None
    if category_slug:
        current_category = Category.objects.filter(slug=category_slug).first()
        products = products.filter(category__slug=category_slug)
    return render(request, 'categories.html', {
        'categories': categories,
        'products': products,
        'current_category': current_category,
    })
