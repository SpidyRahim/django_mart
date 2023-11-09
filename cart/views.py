from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from django.db.models import Q

# Create your views here.
from .models import Cart, CartItem


def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def cart(request):
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    # 1 --- 100
    # 5 --- 100*5
    session_id = get_create_session(request)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        combined_quantities = {}
        for cart_item in cart_items:
            product_id = cart_item.product_id
            if product_id in combined_quantities:
                combined_quantities[product_id] += cart_item.quantity
                # Deactivate the current cart item
                cart_item.is_active = False
                cart_item.save()
            else:
                combined_quantities[product_id] = cart_item.quantity
        for item in cart_items:
            total += item.product.price * item.quantity
    else:
        # session id ke niye aslam
        # model ke ber kore anlam
        cartid = Cart.objects.get(cart_id=session_id)
        # ei session id wala kono cart amader database e ache kina
        cart_id = Cart.objects.filter(cart_id=session_id).exists()
        print(cart_id)
        if cart_id:
            cart_items = CartItem.objects.filter(cart=cartid)
            for item in cart_items:
                total += item.product.price * item.quantity
    print(cart_items)
    tax = (2*total)/100  # 2 % vat
    grand_total = total + tax

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'tax': tax, 'total': total, 'grand_total': grand_total})


def add_to_cart(request, product_id):
    # product = Product.objects.get(id=product_id)
    # session_id = get_create_session(request)  # session id ke ber kore anlam

    # if request.user.is_authenticated:  # logged in
    #     cart_item = CartItem.objects.filter(
    #         product=product, user=request.user).exists()
    #     if cart_item:
    #         item = CartItem.objects.get(product=product)
    #         item.quantity += 1
    #         item.save()
    #     else:
    #         cartid = Cart.objects.get(cart_id=session_id)
    #         item = CartItem.objects.create(
    #             cart=cartid,
    #             product=product,
    #             quantity=1,
    #             user=request.user
    #         )
    #         item.save()

    product = Product.objects.get(id=product_id)
    session_id = get_create_session(request)  # session id ke ber kore anlam

    if request.user.is_authenticated:  # logged in
        cart_item = CartItem.objects.filter(
            product=product, user=request.user).exists()
        if cart_item:
            item = CartItem.objects.get(product=product)
            item.quantity += 1
            item.save()
        else:
            try:
                cartid = Cart.objects.get(cart_id=session_id)
            except Cart.DoesNotExist:
                # If the cart doesn't exist, create a new one
                cartid = Cart.objects.create(cart_id=session_id)
            item = CartItem.objects.create(
                cart=cartid,
                product=product,
                quantity=1,
                user=request.user
            )
            item.save()
    else:
        print(session_id)
        # session id wala kono cart id ache kina check kortechi,Thakle True dibe naile False
        cart_id = Cart.objects.filter(cart_id=session_id).exists()
        if cart_id:  # jodi cart id thake
            cartid = Cart.objects.get(cart_id=session_id)
            cart_item = CartItem.objects.filter(
                product=product, cart=cartid).exists()
            if cart_item:
                item = CartItem.objects.get(product=product, cart=cartid)
                item.quantity += 1
                item.save()
            else:
                cartid = Cart.objects.get(cart_id=session_id)
                print("adfasdf ", cartid, session_id)
                item = CartItem.objects.create(
                    cart=cartid,
                    product=product,
                    quantity=1
                )
                item.save()
        else:
            cart = Cart.objects.create(
                cart_id=session_id
            )
            cart.save()

    return redirect('cart')


def remove_cart_item(request, product_id):
    print(product_id)
    product = Product.objects.get(id=product_id)
    session_id = request.session.session_key
    cartid = Cart.objects.get(cart_id=session_id)  # cart search korlam
    # cart item filter korbo cartid ar product id er upor filter korbo
    cart_item = CartItem.objects.get(cart=cartid, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    print(type(cart_item))
    return redirect('cart')


def remove_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    session_id = request.session.session_key
    cartid = Cart.objects.get(cart_id=session_id)  # cart search korlam
    # cart item filter korbo cartid ar product id er upor filter korbo
    cart_item = CartItem.objects.get(cart=cartid, product=product)
    cart_item.delete()
    return redirect('cart')


def checkout(request):
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    # 1 --- 100
    # 5 --- 100*5
    session_id = get_create_session(request)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        combined_quantities = {}
        for cart_item in cart_items:
            product_id = cart_item.product_id
            if product_id in combined_quantities:
                combined_quantities[product_id] += cart_item.quantity
                # Deactivate the current cart item
                cart_item.is_active = False
                cart_item.save()
            else:
                combined_quantities[product_id] = cart_item.quantity
        for item in cart_items:
            total += item.product.price * item.quantity
    else:
        # session id ke niye aslam
        # model ke ber kore anlam
        cartid = Cart.objects.get(cart_id=session_id)
        # ei session id wala kono cart amader database e ache kina
        cart_id = Cart.objects.filter(cart_id=session_id).exists()
        print(cart_id)
        if cart_id:
            cart_items = CartItem.objects.filter(cart=cartid)
            for item in cart_items:
                total += item.product.price * item.quantity
    print(cart_items)
    tax = (2*total)/100  # 2 % vat
    grand_total = total + tax
    return render(request, 'cart/place-order.html', {'cart_items': cart_items, 'tax': tax, 'total': total, 'grand_total': grand_total})
