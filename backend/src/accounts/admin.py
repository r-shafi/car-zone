from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, BuyerProfile, SellerProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced admin for custom User model"""

    list_display = (
        'username', 'email', 'role', 'is_active',
        'profile_picture_preview', 'date_joined'
    )
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    # Define fieldsets properly as a tuple of tuples
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Car Zone Profile', {
            'fields': ('role', 'phone_number', 'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Define add_fieldsets properly
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Car Zone Profile', {
            'fields': ('role', 'phone_number', 'profile_picture')
        }),
    )

    def profile_picture_preview(self, obj):
        """Display profile picture thumbnail in admin list"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 30px; height: 30px; object-fit: cover; border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return "No Image"

    # Set the short description for the admin column
    profile_picture_preview.short_description = "Profile Picture"  # type: ignore


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    """Admin for Buyer Profile"""

    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Data', {
            'fields': ('saved_searches',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    """Admin for Seller Profile"""

    list_display = ('user', 'company_name', 'rating',
                    'created_at', 'updated_at')
    list_filter = ('rating', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'company_name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Business Information', {
            'fields': ('company_name', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('user')
