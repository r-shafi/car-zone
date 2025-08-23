#!/usr/bin/env python
"""
Seed script to populate the Car Zone database with sample data
This script creates 5-10 records for each model to demonstrate the admin interface
"""
from analytics.models import Analytics, SearchLog
from moderation.models import Report
from messaging.models import Message
from cars.models import Car, CarListing, Favorite
from accounts.models import BuyerProfile, SellerProfile
from django.utils import timezone
from django.contrib.auth import get_user_model
import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append('src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carzone.settings')
django.setup()


User = get_user_model()


def create_users():
    """Create sample users with different roles"""
    print("Creating users...")

    users_data = [
        {
            'username': 'admin_user',
            'email': 'admin@carzone.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'phone_number': '+1234567890'
        },
        {
            'username': 'john_buyer',
            'email': 'john.buyer@email.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'role': 'buyer',
            'phone_number': '+1234567891'
        },
        {
            'username': 'jane_buyer',
            'email': 'jane.buyer@email.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'role': 'buyer',
            'phone_number': '+1234567892'
        },
        {
            'username': 'mike_buyer',
            'email': 'mike.buyer@email.com',
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'role': 'buyer',
            'phone_number': '+1234567893'
        },
        {
            'username': 'sarah_buyer',
            'email': 'sarah.buyer@email.com',
            'first_name': 'Sarah',
            'last_name': 'Wilson',
            'role': 'buyer',
            'phone_number': '+1234567894'
        },
        {
            'username': 'ace_motors',
            'email': 'contact@acemotors.com',
            'first_name': 'David',
            'last_name': 'Miller',
            'role': 'seller',
            'phone_number': '+1234567895'
        },
        {
            'username': 'premium_cars',
            'email': 'sales@premiumcars.com',
            'first_name': 'Lisa',
            'last_name': 'Anderson',
            'role': 'seller',
            'phone_number': '+1234567896'
        },
        {
            'username': 'city_auto',
            'email': 'info@cityauto.com',
            'first_name': 'Robert',
            'last_name': 'Brown',
            'role': 'seller',
            'phone_number': '+1234567897'
        },
        {
            'username': 'luxury_motors',
            'email': 'hello@luxurymotors.com',
            'first_name': 'Emma',
            'last_name': 'Davis',
            'role': 'seller',
            'phone_number': '+1234567898'
        },
        {
            'username': 'budget_cars',
            'email': 'contact@budgetcars.com',
            'first_name': 'Tom',
            'last_name': 'Garcia',
            'role': 'seller',
            'phone_number': '+1234567899'
        }
    ]

    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✓ Created user: {user.username} ({user.role})")
        created_users.append(user)

    return created_users


def create_profiles(users):
    """Create buyer and seller profiles"""
    print("Creating profiles...")

    buyer_profiles_data = [
        {
            'saved_searches': {
                'make': 'Toyota',
                'max_price': 30000,
                'location': 'New York'
            }
        },
        {
            'saved_searches': {
                'fuel_type': 'electric',
                'max_price': 50000,
                'location': 'California'
            }
        },
        {
            'saved_searches': {
                'transmission': 'manual',
                'max_price': 25000,
                'location': 'Texas'
            }
        },
        {
            'saved_searches': {
                'make': 'BMW',
                'min_year': 2018,
                'location': 'Florida'
            }
        },
        {
            'saved_searches': {
                'make': 'Honda',
                'max_mileage': 50000,
                'location': 'Illinois'
            }
        }
    ]

    seller_profiles_data = [
        {'company_name': 'Ace Motors LLC', 'rating': 4.8},
        {'company_name': 'Premium Cars Inc', 'rating': 4.5},
        {'company_name': 'City Auto Sales', 'rating': 4.2},
        {'company_name': 'Luxury Motors Group', 'rating': 4.9},
        {'company_name': 'Budget Cars Direct', 'rating': 4.0}
    ]

    # Create buyer profiles
    buyers = [u for u in users if u.role == 'buyer']
    for i, buyer in enumerate(buyers):
        if i < len(buyer_profiles_data):
            profile, created = BuyerProfile.objects.get_or_create(
                user=buyer,
                defaults=buyer_profiles_data[i]
            )
            if created:
                print(f"✓ Created buyer profile for {buyer.username}")

    # Create seller profiles
    sellers = [u for u in users if u.role == 'seller']
    for i, seller in enumerate(sellers):
        if i < len(seller_profiles_data):
            profile, created = SellerProfile.objects.get_or_create(
                user=seller,
                defaults=seller_profiles_data[i]
            )
            if created:
                print(f"✓ Created seller profile for {seller.username}")


def create_cars():
    """Create sample cars"""
    print("Creating cars...")

    cars_data = [
        {
            'make': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'mileage': 25000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'color': 'Silver',
            'engine_size': '2.5L'
        },
        {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2019,
            'mileage': 30000,
            'fuel_type': 'petrol',
            'transmission': 'manual',
            'color': 'Blue',
            'engine_size': '1.5L'
        },
        {
            'make': 'BMW',
            'model': '3 Series',
            'year': 2021,
            'mileage': 15000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'color': 'Black',
            'engine_size': '2.0L'
        },
        {
            'make': 'Tesla',
            'model': 'Model 3',
            'year': 2022,
            'mileage': 10000,
            'fuel_type': 'electric',
            'transmission': 'automatic',
            'color': 'White',
            'engine_size': 'Electric'
        },
        {
            'make': 'Ford',
            'model': 'F-150',
            'year': 2020,
            'mileage': 35000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'color': 'Red',
            'engine_size': '5.0L'
        },
        {
            'make': 'Mercedes-Benz',
            'model': 'C-Class',
            'year': 2021,
            'mileage': 18000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'color': 'Gray',
            'engine_size': '2.0L'
        },
        {
            'make': 'Audi',
            'model': 'A4',
            'year': 2019,
            'mileage': 28000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'color': 'White',
            'engine_size': '2.0L'
        },
        {
            'make': 'Nissan',
            'model': 'Altima',
            'year': 2020,
            'mileage': 22000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'color': 'Black',
            'engine_size': '2.5L'
        },
        {
            'make': 'Hyundai',
            'model': 'Elantra',
            'year': 2021,
            'mileage': 12000,
            'fuel_type': 'petrol',
            'transmission': 'manual',
            'color': 'Silver',
            'engine_size': '2.0L'
        },
        {
            'make': 'Volkswagen',
            'model': 'Jetta',
            'year': 2019,
            'mileage': 32000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'color': 'Blue',
            'engine_size': '1.4L'
        }
    ]

    created_cars = []
    for car_data in cars_data:
        car, created = Car.objects.get_or_create(
            make=car_data['make'],
            model=car_data['model'],
            year=car_data['year'],
            defaults=car_data
        )
        if created:
            print(f"✓ Created car: {car}")
        created_cars.append(car)

    return created_cars


def create_car_listings(cars, sellers):
    """Create car listings"""
    print("Creating car listings...")

    listings_data = [
        {
            'price': Decimal('28500.00'),
            'description': 'Excellent condition Toyota Camry with low mileage. Well-maintained, single owner.',
            'location': 'New York, NY',
            'status': 'available',
            'views': 45
        },
        {
            'price': Decimal('22000.00'),
            'description': 'Reliable Honda Civic, perfect for city driving. Manual transmission, fuel efficient.',
            'location': 'Los Angeles, CA',
            'status': 'available',
            'views': 32
        },
        {
            'price': Decimal('35000.00'),
            'description': 'Luxury BMW 3 Series in pristine condition. All service records available.',
            'location': 'Chicago, IL',
            'status': 'available',
            'views': 67
        },
        {
            'price': Decimal('42000.00'),
            'description': 'Tesla Model 3 with autopilot, supercharger included. Like new condition.',
            'location': 'San Francisco, CA',
            'status': 'available',
            'views': 89
        },
        {
            'price': Decimal('38000.00'),
            'description': 'Ford F-150 truck, perfect for work or family. Powerful V8 engine.',
            'location': 'Houston, TX',
            'status': 'sold',
            'views': 54
        },
        {
            'price': Decimal('45000.00'),
            'description': 'Mercedes-Benz C-Class sedan with premium package. Exceptional luxury.',
            'location': 'Miami, FL',
            'status': 'available',
            'views': 76
        },
        {
            'price': Decimal('32000.00'),
            'description': 'Audi A4 quattro with all-wheel drive. Perfect for all weather conditions.',
            'location': 'Denver, CO',
            'status': 'pending',
            'views': 41
        },
        {
            'price': Decimal('25000.00'),
            'description': 'Nissan Altima sedan, comfortable and reliable. Great value for money.',
            'location': 'Phoenix, AZ',
            'status': 'available',
            'views': 28
        },
        {
            'price': Decimal('23500.00'),
            'description': 'Hyundai Elantra with excellent warranty coverage. Low mileage, great condition.',
            'location': 'Seattle, WA',
            'status': 'available',
            'views': 36
        },
        {
            'price': Decimal('21000.00'),
            'description': 'Volkswagen Jetta with turbocharged engine. Fun to drive, German engineering.',
            'location': 'Boston, MA',
            'status': 'available',
            'views': 29
        }
    ]

    created_listings = []
    for i, listing_data in enumerate(listings_data):
        if i < len(cars):
            # Cycle through sellers if there are more cars than sellers
            seller = sellers[i % len(sellers)]
            listing, created = CarListing.objects.get_or_create(
                car=cars[i],
                seller=seller,
                defaults=listing_data
            )
            if created:
                print(f"✓ Created listing: {listing}")
            created_listings.append(listing)

    return created_listings


def create_favorites(buyers, listings):
    """Create favorite listings"""
    print("Creating favorites...")

    favorites_data = [
        (0, 0),  # john_buyer likes Toyota Camry
        (0, 2),  # john_buyer likes BMW 3 Series
        (1, 3),  # jane_buyer likes Tesla Model 3
        (1, 5),  # jane_buyer likes Mercedes C-Class
        (2, 1),  # mike_buyer likes Honda Civic
        (2, 6),  # mike_buyer likes Audi A4
        (3, 3),  # sarah_buyer likes Tesla Model 3
        (3, 8),  # sarah_buyer likes Hyundai Elantra
    ]

    for buyer_idx, listing_idx in favorites_data:
        if buyer_idx < len(buyers) and listing_idx < len(listings):
            favorite, created = Favorite.objects.get_or_create(
                user=buyers[buyer_idx],
                listing=listings[listing_idx]
            )
            if created:
                print(
                    f"✓ Created favorite: {buyers[buyer_idx].username} -> {listings[listing_idx].car}")


def create_messages(buyers, sellers, listings):
    """Create messages between buyers and sellers"""
    print("Creating messages...")

    messages_data = [
        {
            'sender_idx': 0,  # john_buyer
            'receiver_idx': 0,  # ace_motors
            'listing_idx': 0,
            'content': 'Hi, I\'m very interested in your Toyota Camry. Is it still available? Can we schedule a test drive?',
            'is_read': True
        },
        {
            'sender_idx': 0,  # ace_motors (seller)
            'receiver_idx': 0,  # john_buyer
            'listing_idx': 0,
            'content': 'Yes, the Camry is still available! I\'d be happy to arrange a test drive. When would be convenient for you?',
            'is_read': False
        },
        {
            'sender_idx': 1,  # jane_buyer
            'receiver_idx': 3,  # luxury_motors
            'listing_idx': 3,
            'content': 'I love the Tesla Model 3! What\'s included with the purchase? Does it have the premium interior package?',
            'is_read': True
        },
        {
            'sender_idx': 2,  # mike_buyer
            'receiver_idx': 1,  # premium_cars
            'listing_idx': 1,
            'content': 'Is the Honda Civic\'s manual transmission in good condition? Any recent repairs?',
            'is_read': True
        },
        {
            'sender_idx': 3,  # sarah_buyer
            'receiver_idx': 4,  # budget_cars
            'listing_idx': 8,
            'content': 'The Hyundai Elantra looks perfect for my needs. What\'s your best price?',
            'is_read': False
        },
        {
            'sender_idx': 0,  # john_buyer
            'receiver_idx': 2,  # city_auto
            'listing_idx': 2,
            'content': 'Beautiful BMW! Can you provide the maintenance history?',
            'is_read': True
        },
        {
            'sender_idx': 1,  # jane_buyer
            'receiver_idx': 3,  # luxury_motors
            'listing_idx': 5,
            'content': 'Interested in the Mercedes C-Class. Can we negotiate on the price?',
            'is_read': False
        },
        {
            'sender_idx': 2,  # mike_buyer
            'receiver_idx': 2,  # city_auto
            'listing_idx': 6,
            'content': 'The Audi A4 is exactly what I\'m looking for. Is financing available?',
            'is_read': True
        }
    ]

    all_users = buyers + sellers
    for msg_data in messages_data:
        sender = all_users[msg_data['sender_idx']] if msg_data['sender_idx'] < len(
            all_users) else buyers[0]

        # Determine receiver - if sender is buyer, receiver is seller and vice versa
        if sender in buyers:
            receiver = sellers[msg_data['receiver_idx']] if msg_data['receiver_idx'] < len(
                sellers) else sellers[0]
        else:
            receiver = buyers[msg_data['receiver_idx']] if msg_data['receiver_idx'] < len(
                buyers) else buyers[0]

        listing = listings[msg_data['listing_idx']] if msg_data['listing_idx'] < len(
            listings) else listings[0]

        message, created = Message.objects.get_or_create(
            sender=sender,
            receiver=receiver,
            listing=listing,
            content=msg_data['content'],
            defaults={'is_read': msg_data['is_read']}
        )
        if created:
            print(
                f"✓ Created message: {sender.username} -> {receiver.username}")


def create_reports(buyers, sellers, listings):
    """Create moderation reports"""
    print("Creating reports...")

    reports_data = [
        {
            'reporter_idx': 0,  # john_buyer
            'reported_listing_idx': 4,  # Ford F-150 (sold)
            'reason': 'fake',
            'description': 'This listing shows as available but I called and they said it was sold weeks ago.',
            'status': 'pending'
        },
        {
            'reporter_idx': 1,  # jane_buyer
            'reported_user_idx': 4,  # budget_cars seller
            'reason': 'scam',
            'description': 'This seller asked for payment before showing the car. Very suspicious behavior.',
            'status': 'reviewed'
        },
        {
            'reporter_idx': 2,  # mike_buyer
            'reported_listing_idx': 7,  # Nissan Altima
            'reason': 'inappropriate',
            'description': 'The description contains misleading information about the car\'s condition.',
            'status': 'resolved'
        },
        {
            'reporter_idx': 3,  # sarah_buyer
            'reported_listing_idx': 9,  # Volkswagen Jetta
            'reason': 'spam',
            'description': 'This looks like a duplicate listing with slightly different prices.',
            'status': 'pending'
        },
        {
            'reporter_idx': 0,  # john_buyer
            'reported_user_idx': 2,  # city_auto seller
            'reason': 'other',
            'description': 'Seller was very rude and unprofessional during our phone conversation.',
            'status': 'dismissed'
        }
    ]

    admin_user = User.objects.filter(role='admin').first()

    for report_data in reports_data:
        reporter = buyers[report_data['reporter_idx']
                          ] if report_data['reporter_idx'] < len(buyers) else buyers[0]

        defaults = {
            'reason': report_data['reason'],
            'description': report_data['description'],
            'status': report_data['status']
        }

        if report_data['status'] in ['reviewed', 'resolved', 'dismissed'] and admin_user:
            defaults['reviewed_by'] = admin_user
            defaults['reviewed_at'] = timezone.now() - timedelta(days=1)

        if 'reported_listing_idx' in report_data:
            listing = listings[report_data['reported_listing_idx']
                               ] if report_data['reported_listing_idx'] < len(listings) else listings[0]
            report, created = Report.objects.get_or_create(
                reporter=reporter,
                reported_listing=listing,
                defaults=defaults
            )
        elif 'reported_user_idx' in report_data:
            reported_user = sellers[report_data['reported_user_idx']
                                    ] if report_data['reported_user_idx'] < len(sellers) else sellers[0]
            report, created = Report.objects.get_or_create(
                reporter=reporter,
                reported_user=reported_user,
                defaults=defaults
            )

        if created:
            print(f"✓ Created report by {reporter.username}")


def create_analytics():
    """Create analytics data"""
    print("Creating analytics...")

    # Create analytics for the last 7 days
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        analytics, created = Analytics.objects.get_or_create(
            date=date,
            defaults={
                'new_users': 2 + i,
                'new_listings': 1 + i,
                'total_views': 50 + (i * 10),
                'new_messages': 3 + i,
                'new_reports': 1 if i % 2 == 0 else 0,
                'search_terms': {
                    'toyota': 15 + i,
                    'honda': 12 + i,
                    'bmw': 8 + i,
                    'tesla': 10 + i,
                    'mercedes': 6 + i
                },
                'top_models': {
                    'Toyota Camry': 25 + i,
                    'Honda Civic': 20 + i,
                    'BMW 3 Series': 18 + i,
                    'Tesla Model 3': 22 + i,
                    'Mercedes C-Class': 15 + i
                },
                'popular_locations': {
                    'New York': 5 + i,
                    'Los Angeles': 4 + i,
                    'Chicago': 3 + i,
                    'San Francisco': 4 + i,
                    'Houston': 2 + i
                }
            }
        )
        if created:
            print(f"✓ Created analytics for {date}")


def create_search_logs(users):
    """Create search logs"""
    print("Creating search logs...")

    search_queries = [
        'Toyota Camry 2020',
        'Honda Civic manual',
        'BMW under 40000',
        'Tesla Model 3',
        'Mercedes luxury sedan',
        'Ford truck 2020',
        'Audi A4 quattro',
        'Nissan reliable car',
        'Hyundai warranty',
        'Volkswagen turbo',
        'electric cars',
        'manual transmission',
        'low mileage cars',
        'luxury sedans',
        'SUV family car'
    ]

    ip_addresses = [
        '192.168.1.100',
        '192.168.1.101',
        '192.168.1.102',
        '192.168.1.103',
        '192.168.1.104',
        '10.0.0.100',
        '10.0.0.101',
        '172.16.0.100'
    ]

    for i, query in enumerate(search_queries):
        # Some searches are from logged-in users, others are anonymous
        user = users[i % len(users)] if i % 3 != 0 else None
        ip = ip_addresses[i % len(ip_addresses)]
        results_count = (i * 3) % 10 + 1  # Vary results count

        search_log, created = SearchLog.objects.get_or_create(
            query=query,
            user=user,
            ip_address=ip,
            defaults={'results_count': results_count}
        )
        if created:
            user_info = user.username if user else 'Anonymous'
            print(f"✓ Created search log: '{query}' by {user_info}")


def main():
    """Main function to run all seeding operations"""
    print("🌱 Starting database seeding...")
    print("=" * 50)

    try:
        # Create all the data
        users = create_users()
        print()

        create_profiles(users)
        print()

        cars = create_cars()
        print()

        # Separate users by role
        buyers = [u for u in users if u.role == 'buyer']
        sellers = [u for u in users if u.role == 'seller']

        listings = create_car_listings(cars, sellers)
        print()

        create_favorites(buyers, listings)
        print()

        create_messages(buyers, sellers, listings)
        print()

        create_reports(buyers, sellers, listings)
        print()

        create_analytics()
        print()

        create_search_logs(users)
        print()

        print("=" * 50)
        print("🎉 Database seeding completed successfully!")
        print()
        print("📊 Summary:")
        print(f"   Users: {User.objects.count()}")
        print(f"   Buyer Profiles: {BuyerProfile.objects.count()}")
        print(f"   Seller Profiles: {SellerProfile.objects.count()}")
        print(f"   Cars: {Car.objects.count()}")
        print(f"   Car Listings: {CarListing.objects.count()}")
        print(f"   Favorites: {Favorite.objects.count()}")
        print(f"   Messages: {Message.objects.count()}")
        print(f"   Reports: {Report.objects.count()}")
        print(f"   Analytics Entries: {Analytics.objects.count()}")
        print(f"   Search Logs: {SearchLog.objects.count()}")
        print()
        print("🔗 Django Admin: http://127.0.0.1:8000/admin/")
        print("👤 Superuser - Username: shafi, Password: shafi")
        print()
        print("💡 Test Users (all passwords: 'password123'):")
        for user in users[:5]:
            print(f"   {user.username} ({user.role}) - {user.email}")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
