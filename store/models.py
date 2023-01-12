from django.db import models
from categories.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=50, unique=True)
    description_1 = models.TextField(max_length=2500, blank=True)
    description_2 = models.TextField(max_length=2500, blank=True)
    description_3 = models.TextField(max_length=2500, blank=True)
    description_4 = models.TextField(max_length=2500, blank=True)
    description_5 = models.TextField(max_length=2500, blank=True)
    description_6 = models.TextField(max_length=2500, blank=True)
    price=models.IntegerField()
    
    def upload_to_category(self, name):
        return f"photos/{self.slug}/{self.product_name}/{name}"

    image_1 = models.ImageField(
        upload_to=upload_to_category
    )
    image_2 = models.ImageField(
        upload_to=upload_to_category, blank=True
    )
    image_3 = models.ImageField(
        upload_to=upload_to_category, blank=True
    )
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def get_url(self):
        return reverse('product_detail',args=[self.slug])
    
    def __str__(self):
        return self.product_name