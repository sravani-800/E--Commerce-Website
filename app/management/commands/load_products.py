from django.core.management.base import BaseCommand
from app.models import Product

class Command(BaseCommand):
    help = "Load initial products into the database"

    def handle(self, *args, **kwargs):
        products = [
            {"product_name": "Laptop", "product_category": "Electronics", "product_price": 700, "product_description": "A high-performance laptop suitable for all your computing needs.", "product_image": "http://127.0.0.1:8000/static/images/laptop.jpg"},
            {"product_name": "Smartphone", "product_category": "Electronics", "product_price": 500, "product_description": "A sleek smartphone with the latest features and excellent performance.", "product_image": "http://127.0.0.1:8000/static/images/smartphone.jpg"},
            {"product_name": "Running Shoes", "product_category": "Sportswear", "product_price": 80, "product_description": "Comfortable running shoes for all-day wear.", "product_image": "http://127.0.0.1:8000/static/images/shoes.jpg"},
            {"product_name": "T-Shirt", "product_category": "Clothing", "product_price": 20, "product_description": "A soft and durable t-shirt for casual wear.", "product_image": "http://127.0.0.1:8000/static/images/tshirt.jpg"},
            {"product_name": "Headphones", "product_category": "Electronics", "product_price": 150, "product_description": "Noise-cancelling headphones with crystal clear audio quality.", "product_image": "http://127.0.0.1:8000/static/images/headphones.jpg"}
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(
                product_name=product_data['product_name'],
                defaults=product_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added product: {product.product_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Product already exists: {product.product_name}"))
