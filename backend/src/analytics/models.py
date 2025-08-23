from django.db import models
from django.utils import timezone


class Analytics(models.Model):

    date = models.DateField(unique=True, db_index=True)
    new_users = models.PositiveIntegerField(default=0)
    new_listings = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    new_messages = models.PositiveIntegerField(default=0)
    new_reports = models.PositiveIntegerField(default=0)
    search_terms = models.JSONField(
        default=dict,
        help_text="Popular search terms with their frequency"
    )
    top_models = models.JSONField(
        default=dict,
        help_text="Most viewed car models with their view counts"
    )
    popular_locations = models.JSONField(
        default=dict,
        help_text="Popular listing locations with counts"
    )
    revenue_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Revenue metrics if applicable"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analytics'
        verbose_name = 'Analytics'
        verbose_name_plural = 'Analytics'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"Analytics for {self.date}"

    @classmethod
    def get_or_create_for_date(cls, date=None):
        if date is None:
            date = timezone.now().date()

        analytics, created = cls.objects.get_or_create(
            date=date,
            defaults={
                'new_users': 0,
                'new_listings': 0,
                'total_views': 0,
                'new_messages': 0,
                'new_reports': 0,
            }
        )
        return analytics, created


class SearchLog(models.Model):

    query = models.CharField(max_length=255)
    results_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='search_logs'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_log'
        verbose_name = 'Search Log'
        verbose_name_plural = 'Search Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['query']),
        ]

    def __str__(self):
        return f"Search: '{self.query}' ({self.results_count} results)"
