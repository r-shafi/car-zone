from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()


class Car(models.Model):

    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]

    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year + 1)
        ]
    )
    mileage = models.PositiveIntegerField(help_text="Mileage in kilometers")
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    transmission = models.CharField(
        max_length=20, choices=TRANSMISSION_CHOICES)
    color = models.CharField(max_length=50)
    engine_size = models.CharField(
        max_length=20, help_text="e.g., '1.8L', '2.0L'")

    class Meta:
        db_table = 'car'
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        indexes = [
            models.Index(fields=['make', 'model']),
            models.Index(fields=['year']),
        ]

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class CarListing(models.Model):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]

    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='listings')
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='car_listings')
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    description = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='available')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'car_listing'
        verbose_name = 'Car Listing'
        verbose_name_plural = 'Car Listings'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
            models.Index(fields=['location']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.car} - ${self.price} ({self.status})"

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Favorite(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey(
        CarListing, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorite'
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        unique_together = ['user', 'listing']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} favorited {self.listing.car}"
