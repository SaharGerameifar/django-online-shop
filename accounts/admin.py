from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OtpCode
from .forms import UserCreateForm, UserChangeForm
from django.contrib.auth.models import Group


class UserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    search_fields = ('email', 'full_name')
    ordering = ('full_name',)
    form = UserChangeForm
    add_form = UserCreateForm
    fieldsets = (
        ('Info', {'fields':('email', 'phone_number', 'full_name', 'password')}),
        ('Permissions', {'fields':('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')})
    )
    add_fieldsets =(
        ('Info', {'fields':('phone_number', 'email', 'full_name', 'password1', 'password2')}),
    )
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)    


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')

