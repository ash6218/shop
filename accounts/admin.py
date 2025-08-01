from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, OtpCode
from django.contrib.auth.models import Group
from django.conf import settings


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'phone_number','full_name', 'is_admin', 'is_superuser']
    list_filter = ['is_admin',]
    readonly_fields = ['last_login']

    fieldsets = [
        [None, {'fields':['email', 'phone_number', 'full_name', 'password', 'address', 'postal_code', 'national_id', 'birthday']}],
        ['permissions', {'fields':['is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions']}]
    ]
    add_fieldsets = [
        [None, {'fields':['phone_number', 'email', 'full_name', 'password1', 'password2']}],
    ]

    search_fields = ['email', 'full_name']
    ordering = ['full_name',]
    filter_horizontal = ['groups', 'user_permissions']

    # we want one of admins to have every permission but cant make themselves superuser.
    # in this case, we shoud override get_form and disable the superuser field.
    # even the superuser themselve cant change this field so we can use an if base on settings.
    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not settings.CCSF:
            form.base_fields['is_superuser'].disabled = True
        return form
    

admin.site.register(User, UserAdmin)


