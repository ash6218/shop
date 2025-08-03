from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.core.validators import RegexValidator

only_digits = RegexValidator(regex=r'^\d+$', message='please enter just numbers')
ten_digits = RegexValidator(regex=r'^\d{10}$', message='please enter exactly 10 digits number')

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    address = models.TextField(max_length=1000, null=True, blank=True, default="")
    postal_code = models.CharField(max_length=10, null=True, blank=True, default="", validators=[ten_digits])
    national_id = models.CharField(max_length=10, null=True, blank=True, default="", validators=[ten_digits])
    birthday = models.DateField(null=True, blank=True, default="1990-01-01")
    image_url = models.URLField(max_length=500, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number' # this fields must have unique=True .
    REQUIRED_FIELDS = ['email', 'full_name'] # only works for createsuperuser. password and USERNAME_FIELD will be asked without being inserted here.

    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin
    

class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
  