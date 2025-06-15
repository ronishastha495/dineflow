# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    list_display = ['id', 'email', 'username', 'user_type', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('user_type',)}),
        ('Restaurant Info', {'fields': ('restaurant_name', 'restaurant_address', 'restaurant_phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Verification', {'fields': ('verification_code',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password1', 'password2',
                'user_type', 'restaurant_name', 'restaurant_address', 'restaurant_phone',
                'is_active', 'is_staff', 'is_superuser'
            ),
        }),
    )
    
    search_fields = ('email', 'username', 'restaurant_name')
    ordering = ('date_joined',)
    filter_horizontal = ('groups', 'user_permissions')