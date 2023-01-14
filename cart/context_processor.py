from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items=CartItem.objects.all().filter(user=request.user)
            else:
                cart_items=CartItem.objects.all().filter(cart=cart[:1])

            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count=0
        
        return dict(cart_count=cart_count)

def cart_current(request):
    total=0
    cart_items=()
    if 'admin' in request.path:
        return {}
    else:
        cart_not_empty=True
        try:
            if request.user.is_authenticated:
                cart_items =CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart,is_active=True)
            if(len(cart_items)!=0):
                cart_not_empty=False
                for cart_item in cart_items:
                    total+=(cart_item.product.price*cart_item.quantity)
                    quantity+=cart_item.quantity
        except Exception as e:
            pass
        
        return dict(cart_not_empty=cart_not_empty,cart_items=cart_items,total=total)