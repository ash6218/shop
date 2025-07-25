from django import forms
from .models import Coupon

class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9, initial=1)

"""class CouponForm(forms.ModelForm):
    class Meta:
        Model = Coupon
        fields = ['code']"""

class CouponForm(forms.Form):
    code = forms.CharField()