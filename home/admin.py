from django.contrib import admin
from .models import Category, Product

from django.contrib import admin
from django import forms
from .models import Product
from bucket import list_s3_images

class ProductAdminForm(forms.ModelForm):
    image_url = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image_choices = list_s3_images()
        self.fields['image_url'].choices = [('', '---------')] + image_choices

admin.site.register(Category)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    readonly_fields = ['image_preview']
    fields = ('name', 'slug', 'price', 'image_url', 'image_preview', 'description', 'category', 'available')



