from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from ckeditor.fields import RichTextField
from accounts.models import User


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['name',]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug,])

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    #image = models.ImageField(upload_to='products/')
    image_url = models.URLField(max_length=500, blank=True, null=True)
    description = RichTextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.slug,])
    
class UploadImage(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product/')

def image_preview(self):
    if self.image_url:
        return mark_safe(f'<img src="{self.image_url}" style="max-height: 150px;">')
    return "-"
image_preview.short_description = "Preview"
Product.image_preview = image_preview

class BucketPics(models.Model):
    image_url = models.URLField(max_length=500, blank=True, null=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments')
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated',]

    def __str__(self):
        return self.title
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ufav')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pfav')
    is_fav = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated',]

    def __str__(self):
        return self.product.name