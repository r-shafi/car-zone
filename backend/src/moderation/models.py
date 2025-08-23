from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Report(models.Model):

    REASON_CHOICES = [
        ('scam', 'Scam'),
        ('spam', 'Spam'),
        ('offensive', 'Offensive Content'),
        ('fake', 'Fake Listing'),
        ('inappropriate', 'Inappropriate'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports_made'
    )
    reported_listing = models.ForeignKey(
        'cars.CarListing',
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True
    )
    reported_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports_received',
        null=True,
        blank=True
    )
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    description = models.TextField(
        blank=True,
        help_text="Additional details about the report"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='reviewed_reports',
        null=True,
        blank=True
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(
        blank=True, help_text="Internal admin notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['reason']),
            models.Index(fields=['created_at']),
            models.Index(fields=['reporter']),
        ]

    def clean(self):
        if not self.reported_listing and not self.reported_user:
            raise ValidationError(
                "Either reported_listing or reported_user must be specified.")

        if self.reporter == self.reported_user:
            raise ValidationError("Reporter cannot report themselves.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        target = ""
        if self.reported_listing:
            target = f"listing '{self.reported_listing.car}'"
        elif self.reported_user:
            target = f"user '{self.reported_user.username}'"

        return f"Report by {self.reporter.username} about {target} ({self.reason})"
