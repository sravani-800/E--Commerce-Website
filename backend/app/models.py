from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField()
    product_image = models.URLField()

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"
