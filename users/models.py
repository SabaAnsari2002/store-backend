from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class BankCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bank_cards')
    card_name = models.CharField(max_length=100, verbose_name="نام کارت")
    card_number = models.CharField(max_length=16, verbose_name="شماره کارت")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.card_name}"

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    title = models.CharField(max_length=100, default='آدرس جدید')
    address_line = models.TextField()
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
