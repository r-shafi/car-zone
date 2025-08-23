from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin for Report model"""

    list_display = (
        'reporter', 'target_info', 'reason', 'status',
        'reviewed_by', 'created_at'
    )
    list_filter = ('reason', 'status', 'created_at', 'reviewed_at')
    search_fields = (
        'reporter__username', 'reporter__email',
        'reported_user__username', 'reported_user__email',
        'reported_listing__car__make', 'reported_listing__car__model',
        'description', 'admin_notes'
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Report Information', {
            'fields': ('reporter', 'reason', 'description')
        }),
        ('Reported Content', {
            'fields': ('reported_listing', 'reported_user')
        }),
        ('Review Status', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'reviewed_at')

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related(
            'reporter', 'reported_user', 'reviewed_by',
            'reported_listing', 'reported_listing__car'
        )

    def target_info(self, obj):
        """Display what was reported"""
        if obj.reported_listing:
            return format_html(
                'Listing: <a href="/admin/cars/carlisting/{}/change/">{}</a>',
                obj.reported_listing.id,
                f"{obj.reported_listing.car} - ${obj.reported_listing.price}"
            )
        elif obj.reported_user:
            return format_html(
                'User: <a href="/admin/accounts/user/{}/change/">{}</a>',
                obj.reported_user.id,
                obj.reported_user.username
            )
        return "Unknown"
    target_info.short_description = 'Reported Target'  # type: ignore

    actions = ['mark_as_reviewed', 'mark_as_resolved', 'mark_as_dismissed']

    def mark_as_reviewed(self, request, queryset):
        """Admin action to mark reports as reviewed"""
        updated = queryset.filter(status='pending').update(
            status='reviewed',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(
            request,
            f"{updated} report(s) marked as reviewed."
        )
    mark_as_reviewed.short_description = "Mark selected reports as reviewed"  # type: ignore

    def mark_as_resolved(self, request, queryset):
        """Admin action to mark reports as resolved"""
        updated = queryset.exclude(status='resolved').update(
            status='resolved',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(
            request,
            f"{updated} report(s) marked as resolved."
        )
    mark_as_resolved.short_description = "Mark selected reports as resolved"  # type: ignore

    def mark_as_dismissed(self, request, queryset):
        """Admin action to mark reports as dismissed"""
        updated = queryset.exclude(status='dismissed').update(
            status='dismissed',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(
            request,
            f"{updated} report(s) marked as dismissed."
        )
    mark_as_dismissed.short_description = "Mark selected reports as dismissed"  # type: ignore

    def save_model(self, request, obj, form, change):
        """Auto-set reviewed_by and reviewed_at when status changes"""
        if change and 'status' in form.changed_data:
            if obj.status in ['reviewed', 'resolved', 'dismissed'] and not obj.reviewed_by:
                obj.reviewed_by = request.user
                obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)
