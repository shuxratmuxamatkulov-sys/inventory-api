from django.db import models
from django.contrib.auth.models import User

# Mahsulot kategoriyalari
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Mahsulotlar jadvali
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Kategoriya")
    name = models.CharField(max_length=150, verbose_name="Mahsulot nomi")
    quantity = models.IntegerField(default=0, verbose_name="Mavjud miqdor")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.quantity} ta"

# Kirim-Chiqim operatsiyalari (Transaction)
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'Kirim'),
        ('OUT', 'Chiqim'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions', verbose_name="Mahsulot")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Mas'ul xodim")
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES, verbose_name="Amal turi")
    quantity = models.IntegerField(verbose_name="Miqdor")
    note = models.TextField(blank=True, null=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} | {self.get_type_display()} | {self.quantity}"