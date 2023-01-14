from django.db import models
from categories.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=50, unique=True)
    brief = models.TextField(max_length=2500, blank=True)
    description = models.TextField(max_length=2500, blank=True)

    price=models.IntegerField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def upload_to_category_img(self, name):
        return f"photos/{self.category}/{self.product_name}/img/{name}"

    def upload_to_category_features(self, name):
        return f"photos/{self.category}/{self.product_name}/features/{name}"

    image_1 = models.ImageField(
        upload_to=upload_to_category_img
    )
    image_2 = models.ImageField(
        upload_to=upload_to_category_img
    )
    image_3 = models.ImageField(
        upload_to=upload_to_category_img
    )

    feature_1_title=models.CharField(max_length=200)
    feature_image_1 = models.ImageField(
        upload_to=upload_to_category_features
    )
    feature_1_description=models.TextField(max_length=2500, blank=True)
    feature_2_title=models.CharField(max_length=200)
    feature_image_2 = models.ImageField(
        upload_to=upload_to_category_features
    )
    feature_2_description=models.TextField(max_length=2500, blank=True)
    feature_3_title=models.CharField(max_length=200)
    feature_image_3 = models.ImageField(
        upload_to=upload_to_category_features
    )
    feature_3_description=models.TextField(max_length=2500, blank=True)
    weight=models.IntegerField()
    dimension_x=models.IntegerField()
    dimension_y=models.IntegerField()
    dimension_z=models.IntegerField()
    warranty=models.IntegerField()
    materials=models.CharField(max_length=200)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    
    def get_url(self):
        return reverse('product_detail',args=[self.slug])
    
    def __str__(self):
        return self.product_name