from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class MyAdminSite(admin.AdminSite):
    site_header = "ABC Company Administrator"
    site_title = "ABC Company Admin"
    index_title = "Welcome to the ABC Company Inventory Administrator Dashboard"
    site_url = "/index/"

admin_site = MyAdminSite(name='myadmin')


User = get_user_model()

class UserCreation(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

class UserChange(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'password', 'role')

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
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

admin.site.register(User, UserAdmin)
admin_site.register(User, UserAdmin)

