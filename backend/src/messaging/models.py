from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Message(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    listing = models.ForeignKey(
        'cars.CarListing',
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True,
        help_text="Optional: message related to a specific listing"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'message'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sender', 'timestamp']),
            models.Index(fields=['receiver', 'timestamp']),
            models.Index(fields=['listing']),
            models.Index(fields=['is_read']),
        ]

    def clean(self):
        if self.sender == self.receiver:
            raise ValidationError(
                "Sender and receiver cannot be the same user.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        listing_info = f" (about {self.listing.car})" if self.listing else ""
        return f"Message from {self.sender.username} to {self.receiver.username}{listing_info}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
