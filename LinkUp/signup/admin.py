from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Link

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'phone_number','name','address','gender','profile_photo', 'is_active', 'is_staff')
    search_fields = ('id', 'email', 'phone_number')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Removed 'username' from fields
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    filter_horizontal = ()  # Remove references to 'groups' and 'user_permissions'
    ordering = ('email',)  # Change ordering to use existing field

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Link)