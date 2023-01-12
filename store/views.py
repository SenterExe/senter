from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def store(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        "products": products,
    }
    return render(request, "store/store.html", context)


def product_detail(request, product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug)
    except Exception as e:
        raise e

    image_urls=[]
    description_content=[]
    if(single_product.description_1 !=""):
        description_content.append(single_product.description_1)
    if(single_product.description_2 !=""):
        description_content.append(single_product.description_2)
    if(single_product.description_3 !=""):
        description_content.append(single_product.description_3)
    if(single_product.description_4 !=""):
        description_content.append(single_product.description_4)
    if(single_product.description_5 !=""):
        description_content.append(single_product.description_5)
    if(single_product.description_6 !=""):
        description_content.append(single_product.description_6)
    if(str(single_product.image_2.url)!=""):
        image_urls.append(single_product.image_2.url)
    if(str(single_product.image_3.url)!=""):
        image_urls.append(single_product.image_3.url)
    context = {
        "product": single_product,
        "images": image_urls,
        "descriptions": description_content,
    }
    return render(request, "store/single.html", context)
