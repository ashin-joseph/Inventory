from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from Sales.models import salesorderTable, returnSalesTable
from Purchase.models import confirmPurchaseTable


class MyAdminSite(admin.AdminSite):
    site_header = "StockSmart"
    site_title = "StockSmart Admin"
    index_title = "Add Staff"
    site_url = "/index/"

admin_site = MyAdminSite(name='myadmin')


User = get_user_model()

class UserCreation(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role','organization')

class UserChange(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'password', 'role', 'organization')

class UserAdmin(BaseUserAdmin):
    add_form = UserCreation
    form = UserChange
    model = User

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Role', {'fields': ('role',)}),
        ('Organization', {'fields': ('organization',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'organization'),
        }),
    )

admin.site.register(User, UserAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(salesorderTable)
admin_site.register(returnSalesTable)
admin_site.register(confirmPurchaseTable)

