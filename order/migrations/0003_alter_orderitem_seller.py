# Generated by Django 5.2.1 on 2025-06-05 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_total_price'),
        ('sellers', '0003_alter_seller_options_alter_seller_shop_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sellers.seller'),
        ),
    ]
