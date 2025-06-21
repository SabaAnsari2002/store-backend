from django.db import models
from django.conf import settings

class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'فروشنده'
        verbose_name_plural = 'فروشندگان'