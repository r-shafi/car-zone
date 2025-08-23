from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Car, CarListing, Favorite


class CarListingInline(admin.TabularInline):
    """Inline admin for CarListing within Car admin"""
    model = CarListing
    extra = 0
    readonly_fields = ('views', 'created_at', 'updated_at')
    fields = ('seller', 'price', 'status', 'views', 'created_at')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Admin for Car model"""

    list_display = (
        'year', 'make', 'model', 'fuel_type', 'transmission',
        'color', 'mileage', 'listing_count'
    )
    list_filter = ('make', 'fuel_type', 'transmission', 'year')
    search_fields = ('make', 'model', 'color')
    ordering = ('-year', 'make', 'model')

    fieldsets = (
        ('Basic Information', {
            'fields': ('make', 'model', 'year', 'color')
        }),
        ('Technical Specifications', {
            'fields': ('fuel_type', 'transmission', 'engine_size', 'mileage')
        }),
    )

    inlines = [CarListingInline]

    def get_queryset(self, request):
        """Optimize queryset with annotation"""
        queryset = super().get_queryset(request)
        return queryset.annotate(listing_count=Count('listings'))

    def listing_count(self, obj):
        """Display number of listings for this car"""
        return obj.listing_count
    listing_count.short_description = 'Listings'  # type: ignore
    listing_count.admin_order_field = 'listing_count'  # type: ignore


@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    """Admin for CarListing model"""

    list_display = (
        'car_info', 'seller', 'price', 'status', 'location',
        'views', 'favorites_count', 'created_at'
    )
    list_filter = ('status', 'car__make', 'car__fuel_type', 'created_at')
    search_fields = (
        'car__make', 'car__model', 'seller__username',
        'seller__email', 'location', 'description'
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Car Information', {
            'fields': ('car',)
        }),
        ('Listing Details', {
            'fields': ('seller', 'price', 'description', 'location', 'status')
        }),
        ('Statistics', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('views', 'created_at', 'updated_at')

    def get_queryset(self, request):
        """Optimize queryset with select_related and annotations"""
        queryset = super().get_queryset(request)
        return queryset.select_related('car', 'seller').annotate(
            favorites_count=Count('favorited_by')
        )

    def car_info(self, obj):
        """Display formatted car information"""
        return f"{obj.car.year} {obj.car.make} {obj.car.model}"
    car_info.short_description = 'Car'  # type: ignore
    car_info.admin_order_field = 'car__make'  # type: ignore

    def favorites_count(self, obj):
        """Display number of users who favorited this listing"""
        return obj.favorites_count
    favorites_count.short_description = 'Favorites'  # type: ignore
    favorites_count.admin_order_field = 'favorites_count'  # type: ignore

    actions = ['mark_as_sold', 'mark_as_available']

    def mark_as_sold(self, request, queryset):
        """Admin action to mark listings as sold"""
        updated = queryset.update(status='sold')
        self.message_user(
            request,
            f"{updated} listing(s) marked as sold."
        )
    mark_as_sold.short_description = "Mark selected listings as sold"  # type: ignore

    def mark_as_available(self, request, queryset):
        """Admin action to mark listings as available"""
        updated = queryset.update(status='available')
        self.message_user(
            request,
            f"{updated} listing(s) marked as available."
        )
    mark_as_available.short_description = "Mark selected listings as available"  # type: ignore


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin for Favorite model"""

    list_display = ('user', 'listing_info', 'created_at')
    list_filter = ('created_at', 'listing__status')
    search_fields = (
        'user__username', 'user__email',
        'listing__car__make', 'listing__car__model'
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'listing', 'listing__car')

    def listing_info(self, obj):
        """Display formatted listing information"""
        return f"{obj.listing.car} - ${obj.listing.price}"
    listing_info.short_description = 'Listing'  # type: ignore
    listing_info.admin_order_field = 'listing__car__make'  # type: ignore
