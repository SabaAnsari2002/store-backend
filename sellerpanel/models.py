from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در حال پردازش'),
        ('delivered', 'تحویل شده'),
        ('cancelled', 'لغو شده'),
    ]

    customer_name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.customer_name} - {self.amount} تومان"
