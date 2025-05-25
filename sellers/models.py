from django.db import models
from users.models import CustomUser

class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    description = models.TextField(blank=True)