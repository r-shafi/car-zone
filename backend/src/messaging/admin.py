from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Q
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin for Message model"""

    list_display = (
        'sender', 'receiver', 'listing_info', 'content_preview',
        'is_read', 'timestamp'
    )
    list_filter = ('is_read', 'timestamp', 'listing__status')
    search_fields = (
        'sender__username', 'sender__email',
        'receiver__username', 'receiver__email',
        'content', 'listing__car__make', 'listing__car__model'
    )
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('Message Information', {
            'fields': ('sender', 'receiver', 'listing')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Status', {
            'fields': ('is_read', 'timestamp'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('timestamp',)

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('sender', 'receiver', 'listing', 'listing__car')

    def listing_info(self, obj):
        """Display formatted listing information"""
        if obj.listing:
            return format_html(
                '<a href="/admin/cars/carlisting/{}/change/">{}</a>',
                obj.listing.id,
                f"{obj.listing.car} - ${obj.listing.price}"
            )
        return "No listing"
    listing_info.short_description = 'Related Listing'  # type: ignore
    listing_info.admin_order_field = 'listing__car__make'  # type: ignore

    def content_preview(self, obj):
        """Display truncated content preview"""
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    content_preview.short_description = 'Content Preview'  # type: ignore

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        """Admin action to mark messages as read"""
        updated = queryset.update(is_read=True)
        self.message_user(
            request,
            f"{updated} message(s) marked as read."
        )
    mark_as_read.short_description = "Mark selected messages as read"  # type: ignore

    def mark_as_unread(self, request, queryset):
        """Admin action to mark messages as unread"""
        updated = queryset.update(is_read=False)
        self.message_user(
            request,
            f"{updated} message(s) marked as unread."
        )
    mark_as_unread.short_description = "Mark selected messages as unread"  # type: ignore
