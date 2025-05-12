from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from django.views import View
from main.models import Product, ProductSpecialist, Specialist


def cart_detail(request):
    """Pass cart object to the html page"""
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


def cart_add(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=item_id)
    specialist = request.POST.get('specialist')

    if specialist:
        try:
            specialist_obj = Specialist.objects.get(name=specialist)
            product_specialist = ProductSpecialist.objects.get(
                product=product,
                specialist=specialist_obj
            )
        except Specialist.DoesNotExist:
            print('specialist does not exist')
            return redirect('cart:cart_detail')
        except ProductSpecialist.DoesNotExist:
            print('product does not exist')
            return redirect('cart:cart_detail')
    else:
        # if specialist is gone replace him 
        # available_specialists = product.specialist
        available_specialists = ProductSpecialist.objects.filter(
            product=product)
        if available_specialists.exists():
            specialist_obj = available_specialists.first().specialist
            specialist = specialist_obj.name
        else:
            return redirect('cart:cart_detail')
    
    cart.add(product, specialist)
    return redirect('cart:cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=item_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


class CartUpdateView(View):
    def post(self, request, item_id):
        cart = Cart(request)
        quantity = request.POST.get("quantity", 1)
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
        prodcut = get_object_or_404(Product, id=item_id)

        if quantity > 0:
            cart.add(prodcut, cart.cart[str(item_id)]['specialist'], quantity)
        else:
            cart.remove(prodcut)

        return redirect('cart:cart_detail')