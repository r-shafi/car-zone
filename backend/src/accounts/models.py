from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):

    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
        ('superadmin', 'Super Admin'),
    ]

    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='buyer')
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.email})"


class BuyerProfile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='buyer_profile')
    saved_searches = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'buyer_profile'
        verbose_name = 'Buyer Profile'
        verbose_name_plural = 'Buyer Profiles'

    def __str__(self):
        return f"Buyer: {self.user.username}"


class SellerProfile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='seller_profile')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(
        default=0.0, help_text="Average rating from buyers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'seller_profile'
        verbose_name = 'Seller Profile'
        verbose_name_plural = 'Seller Profiles'

    def __str__(self):
        return f"Seller: {self.user.username}" + (f" ({self.company_name})" if self.company_name else "")
