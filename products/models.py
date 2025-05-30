from django.db import models
from sellers.models import Seller

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        verbose_name = 'زیردسته‌بندی'
        verbose_name_plural = 'زیردسته‌بندی‌ها'

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)    
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'