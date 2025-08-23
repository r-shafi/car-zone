from django.contrib import admin
from django.utils.html import format_html
import json
from .models import Analytics, SearchLog


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    """Admin for Analytics model"""

    list_display = (
        'date', 'new_users', 'new_listings', 'total_views',
        'new_messages', 'new_reports', 'top_search_terms'
    )
    list_filter = ('date', 'created_at')
    search_fields = ('date',)
    ordering = ('-date',)
    date_hierarchy = 'date'

    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('User Metrics', {
            'fields': ('new_users',)
        }),
        ('Content Metrics', {
            'fields': ('new_listings', 'total_views')
        }),
        ('Engagement Metrics', {
            'fields': ('new_messages', 'new_reports')
        }),
        ('Popular Data', {
            'fields': ('search_terms', 'top_models', 'popular_locations'),
            'classes': ('collapse',)
        }),
        ('Revenue Data', {
            'fields': ('revenue_data',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def top_search_terms(self, obj):
        """Display top 3 search terms"""
        if obj.search_terms:
            # Sort by frequency and take top 3
            sorted_terms = sorted(
                obj.search_terms.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            terms = [f"{term} ({count})" for term, count in sorted_terms]
            return ", ".join(terms) if terms else "No data"
        return "No data"
    top_search_terms.short_description = 'Top Search Terms'  # type: ignore

    def get_readonly_fields(self, request, obj=None):
        """Make date readonly for existing objects"""
        if obj:  # Editing existing object
            return ('created_at', 'updated_at', 'date')
        return ('created_at', 'updated_at')


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    """Admin for SearchLog model"""

    list_display = (
        'query', 'results_count', 'user_info', 'ip_address', 'timestamp'
    )
    list_filter = ('timestamp', 'results_count')
    search_fields = ('query', 'user__username', 'user__email', 'ip_address')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('Search Information', {
            'fields': ('query', 'results_count')
        }),
        ('User Information', {
            'fields': ('user', 'ip_address')
        }),
        ('Timestamp', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('timestamp',)

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('user')

    def user_info(self, obj):
        """Display user information or anonymous"""
        if obj.user:
            return format_html(
                '<a href="/admin/accounts/user/{}/change/">{}</a>',
                obj.user.id,
                obj.user.username
            )
        return "Anonymous"
    user_info.short_description = 'User'  # type: ignore
    user_info.admin_order_field = 'user__username'  # type: ignore

    def has_add_permission(self, request):
        """Disable manual addition of search logs"""
        return False

    def has_change_permission(self, request, obj=None):
        """Make search logs read-only"""
        return False
