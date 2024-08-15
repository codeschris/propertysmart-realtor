from django.core.management.base import BaseCommand
from property.models import Property, User
from faker import Faker
import random
import os
from django.core.files import File

class Command(BaseCommand):
    help = 'Seeds the database with a specified number of property records'

    def add_arguments(self, parser):
        parser.add_argument('num_properties', type=int, help='The number of properties to seed into the database')

    def handle(self, *args, **kwargs):
        num_properties = kwargs['num_properties']
        fake = Faker()

        # Predefined details
        predefined_details = {
            'locations': ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret'],
            'property_types': ['Apartment', 'Villa', 'Bungalow', 'Condo', 'Cottage'],
            'prices': [5000000, 10000000, 15000000, 20000000, 25000000],
            'bedrooms': [2, 3, 4, 5, 6],
            'bathrooms': [1, 2, 3, 4, 5],
            'areas': [1000, 1500, 2000, 2500, 3000],
            'images': [
                'house_1.jpeg',
                'house_2.jpeg',
                'house_3.jpeg',
                'house_4.jpeg',
                'house_5.jpeg',
                'house_6.jpeg',
                'house_7.jpeg'
            ]
        }

        realtors = User.objects.filter(user_type='Realtor')
        if not realtors.exists():
            self.stdout.write(self.style.ERROR('No realtors found. Please create some realtors first.'))
            return

        for _ in range(num_properties):
            location = random.choice(predefined_details['locations'])
            property_type = random.choice(predefined_details['property_types'])

            # Create a more descriptive text for the property
            description = (
                f"Discover your dream home in {location}! This {property_type.lower()} offers unparalleled comfort "
                "with spacious rooms, modern amenities, and a serene environment. Experience the ultimate in luxury living "
                "with features designed to meet your every need. This is the home where comfort meets elegance—truly a dreamhouse "
                "you’ve always wanted."
            )

            property = Property(
                title=f"Houses for rent/sale in {location}",
                description=description,
                price=random.choice(predefined_details['prices']),
                location=location,
                property_type=property_type,
                bedrooms=random.choice(predefined_details['bedrooms']),
                bathrooms=random.choice(predefined_details['bathrooms']),
                area=random.choice(predefined_details['areas']),
                realtor=random.choice(realtors)
            )

            # Assign a random image from the local directory
            image_name = random.choice(predefined_details['images'])
            image_path = os.path.join('property_images', image_name)
            property.primary_photo.save(image_name, File(open(image_path, 'rb')))
            property.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {num_properties} properties into the database'))
