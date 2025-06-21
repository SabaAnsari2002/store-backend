from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from sellers.models import Seller

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'باز'),
        ('in_progress', 'در حال بررسی'),
        ('answered', 'پاسخ داده شده'),
        ('closed', 'بسته شده'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
    ]
    
    CATEGORY_CHOICES = [
        ('technical', 'فنی'),
        ('financial', 'مالی'),
        ('order', 'سفارش'),
        ('other', 'سایر'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='technical')
    order_id = models.CharField(max_length=50, blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status)

    def get_priority_display(self):
        return dict(self.PRIORITY_CHOICES).get(self.priority)

    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category)

    def __str__(self):
        return f"تیکت {self.id} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت‌ها'


class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    is_staff_reply = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"پاسخ {self.id} به تیکت {self.ticket.id}"

    class Meta:
        ordering = ['created_at']
        verbose_name = 'پاسخ تیکت'
        verbose_name_plural = 'پاسخ‌های تیکت'


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='تلفن همراه')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

class Discount(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    percentage = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    for_first_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.seller.user.username if self.seller else 'سیستمی'})"

    def remaining_time(self):
        from django.utils import timezone
        expiry_date = self.created_at + timezone.timedelta(days=2)
        remaining = expiry_date - timezone.now()
        
        if remaining.total_seconds() <= 0:
            return "منقضی شده"
        
        days = remaining.days
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        
        if days > 0:
            return f"{days} روز و {hours} ساعت"
        elif hours > 0:
            return f"{hours} ساعت و {minutes} دقیقه"
        else:
            return f"{minutes} دقیقه"

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
    
class Store(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='owned_stores')
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name='فروشگاه'
        verbose_name_plural='فروشگاه ها'
        
    def __str__(self):
        return self.name
    
class StoreRole(models.Model):
    ROLE_CHOICES = [
        ('cashier', 'صندوق دار'),
        ('warehouse', 'انباردار'),
        ('support', 'پشتیبان'),
        ('manager', 'مدیر فروشگاه'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seller = models.ForeignKey('sellers.Seller', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='نقش'
        verbose_name_plural='نقش ها'
        unique_together = ('user', 'seller')

    def __str__(self):
        return f'{self.user.username} - {self.seller.shop_name} - {self.role}'