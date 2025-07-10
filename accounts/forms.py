from django import forms
from .models import User
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

    # let's see it works???!!!
    def clean_password2(self):
        cd = self.cleaned_data
        p1 = cd['password1']
        p2 = cd['password2']
        if p1 and p2 and p1!=p2:
            raise ValidationError('Passwords must match!')
        return p2

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