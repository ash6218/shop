from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm): # for creating a new form in admin panel
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    # as double password confirmation is not defined in our User model, we did it manually.
    # other fields that already exist in our User model, should be defined with Meta class.
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name']

    def clean_password2(self):
        cd = self.cleaned_data
        p1 = cd['password1']
        p2 = cd['password2']
        if p1 and p2 and p1!=p2:
            raise ValidationError('Passwords must match!')
        return p2

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists.')
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('This phone number already exists.')
        OtpCode.objects.filter(phone_number=phone_number).delete()
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm): # for changing a new form in admin panel
    password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form<a/>")
    # with ReadOnlyPasswordHashField, user cant see or change password dirctly, instead they can use the link provided.
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'last_login']
        # last_login is already exists in our User model

"""
class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField(label='full name')
    phone = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)
""" # didnt use it, as we already had UserCreationForm and used it instead

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

class UserOtpLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        OtpCode.objects.filter(phone_number=phone_number).delete()
        return phone_number