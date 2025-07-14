from django.db import models
from decimal import Decimal

class NetworkNode(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=20)
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients'
    )
    debt_to_supplier = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

    @property
    def level(self):
        if not self.supplier:
            return 0
        return self.supplier.level + 1

class Product(models.Model):
    node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name='products'
    )
    title = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.title} {self.model}"
