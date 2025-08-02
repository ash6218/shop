from django.contrib import admin
from .models import Category, Product, Comment, Favorite
from django.contrib import admin
from django import forms
from .models import Product
from bucket import list_s3_images


"""class CategoryAdminForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image_choices = list_s3_images()
        self.fields['image_url'].choices = [('', '---------')] + image_choices
"""
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_sub',)
    ordering = ['is_sub','name']

class ProductAdminForm(forms.ModelForm):
    image_url = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image_choices = list_s3_images()[0]
        self.fields['image_url'].choices = [('', '---------')] + image_choices

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    readonly_fields = ['image_preview']
    fields = ('name', 'slug', 'price', 'image_url', 'image_preview', 'description', 'category', 'available')
    raw_id_fields = ['category']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'title', 'text', 'created', 'updated',)
    ordering = ['updated']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'is_fav', 'created', 'updated',)
    ordering = ['is_fav', '-updated']

