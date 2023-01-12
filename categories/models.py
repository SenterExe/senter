from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.CharField(max_length=700)

    def upload_to_category(self, name):
        return f"photos/{self.slug}/{name}"

    category_image = models.ImageField(
        upload_to=upload_to_category, blank=True
    )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name
