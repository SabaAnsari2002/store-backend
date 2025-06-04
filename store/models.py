from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Store(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام فروشگاه'),
        help_text=_('نام کامل فروشگاه را وارد کنید')
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('مالک فروشگاه'),
        related_name='stores'
    )
    rating = models.FloatField(
        default=0,
        verbose_name=_('امتیاز'),
        help_text=_('امتیاز فروشگاه بین 0 تا 5')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاریخ ایجاد')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاریخ بروزرسانی')
    )

    products = models.ManyToManyField(
        Product,
        through='StoreProduct',
        verbose_name=_('محصولات')
    )

    class Meta:
        verbose_name = _('فروشگاه')
        verbose_name_plural = _('فروشگاه‌ها')
        ordering = ['-rating', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"{self.name} (امتیاز: {self.rating})"

    @property
    def available_products_count(self):
        return self.products.filter(storeproduct__stock__gt=0).count()


class StoreProduct(models.Model):
    class DeliveryTimeChoices(models.TextChoices):
        EXPRESS = 'express', _('اکسپرس (1-2 روز کاری)')
        STANDARD = 'standard', _('معمولی (3-5 روز کاری)')
        LONG = 'long', _('زمانبر (بیش از 5 روز کاری)')

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        verbose_name=_('فروشگاه'),
        related_name='store_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('محصول'),
        related_name='product_stores'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('قیمت')
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name=_('موجودی')
    )
    delivery_time = models.CharField(
        max_length=50,
        choices=DeliveryTimeChoices.choices,
        default=DeliveryTimeChoices.STANDARD,
        verbose_name=_('زمان تحویل')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('فعال')
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('آخرین بروزرسانی')
    )

    class Meta:
        verbose_name = _('محصول فروشگاه')
        verbose_name_plural = _('محصولات فروشگاه‌ها')
        unique_together = [['store', 'product']]
        ordering = ['-last_updated']
        indexes = [
            models.Index(fields=['store', 'product']),
            models.Index(fields=['price']),
            models.Index(fields=['stock']),
        ]

    def __str__(self):
        return f"{self.product.name} در {self.store.name} - قیمت: {self.price}"

    @property
    def availability_status(self):
        if self.stock > 10:
            return _('موجود')
        elif self.stock > 0:
            return _('کم موجود')
        return _('ناموجود')