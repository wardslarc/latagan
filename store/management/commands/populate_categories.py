from django.core.management.base import BaseCommand
from store.models import Category


class Command(BaseCommand):
    help = 'Populate database with default categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Clothing & Apparel',
                'description': 'Vintage and secondhand clothing, jackets, dresses, shirts, and more'
            },
            {
                'name': 'Footwear',
                'description': 'Shoes, boots, sneakers, and other footwear'
            },
            {
                'name': 'Accessories',
                'description': 'Belts, bags, hats, scarves, and fashion accessories'
            },
            {
                'name': 'Electronics',
                'description': 'Used electronics, gadgets, and devices'
            },
            {
                'name': 'Home & Furniture',
                'description': 'Furniture, decor, kitchen items, and home goods'
            },
            {
                'name': 'Books & Media',
                'description': 'Books, vinyl records, CDs, DVDs, and magazines'
            },
            {
                'name': 'Jewelry',
                'description': 'Vintage and secondhand jewelry, watches, and accessories'
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Sporting equipment, outdoor gear, and athletic wear'
            },
            {
                'name': 'Collectibles',
                'description': 'Collectible items, vintage finds, and rare pieces'
            },
            {
                'name': 'Other',
                'description': 'Miscellaneous items that don\'t fit other categories'
            },
        ]

        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated categories!')
        )
