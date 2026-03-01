from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=20, unique=True)
    stock = models.PositiveIntegerField()
    price = models.FloatField()
    tax_percentage = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.product_id})"


class Purchase(models.Model):
    customer_email = models.EmailField()
    total_without_tax = models.FloatField()
    total_tax = models.FloatField()
    net_price = models.FloatField()
    paid_amount = models.FloatField()
    balance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.FloatField()
    tax_amount = models.FloatField()
    total_price = models.FloatField()