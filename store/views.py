from django.shortcuts import render, get_object_or_404
from .models import Product
from cart.models import CartItem

from cart.views import _cart_id
# Create your views here.


def store(request):
    products = Product.objects.all().filter(is_available=True).order_by('id')
    context = {
        "products": products,
    }
    return render(request, "store/store.html", context)


def product_detail(request, product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        "product": single_product,
        "in_cart":in_cart,
    }
    return render(request, "store/single.html", context)
 
def search(request):
    product=[]
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            product=Product.objects.order_by('id').filter(brief__icontains=keyword) | Product.objects.order_by('id').filter(description__icontains=keyword) | Product.objects.order_by('id').filter(feature_1_description__icontains=keyword) | Product.objects.order_by('id').filter(feature_2_description__icontains=keyword) | Product.objects.order_by('id').filter(feature_3_description__icontains=keyword) | Product.objects.order_by('id').filter(product_name__icontains=keyword) 
    context = {
       "products" : product,
    }
    return render(request, "store/store.html", context)