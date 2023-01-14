from .models import Product

def products_list(request):
    products=Product.objects.all().order_by('id')[:3]
    return dict(products=products)