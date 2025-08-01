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
 
class UserChagePasswordForm(forms.Form):
    password = forms.CharField(label='old password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='new password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm new password', widget=forms.PasswordInput)
    

    def clean_password2(self):
        cd = self.cleaned_data
        p1 = cd['password1']
        p2 = cd['password2']
        if p1 and p2 and p1!=p2:
            raise ValidationError('Passwords must match!')
        elif len(p1)<8 or len(p2)<8:
            raise ValidationError('Password must have at least 8 characters!')
        return p2
    
    def __init__(self, *args, **kwargs):
        super(UserChagePasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    
class UserUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'full_name', 'address', 'postal_code', 'national_id', 'birthday']
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            #field.widget.attrs['readonly'] = 'readonly'