# Generated by Django 5.2.3 on 2025-06-27 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sellers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('cashier', 'صندوق دار'), ('warehouse', 'انباردار'), ('support', 'پشتیبان'), ('manager', 'مدیر فروشگاه')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_roles', to='sellers.seller')),
            ],
            options={
                'verbose_name': 'نقش فروشگاه',
                'verbose_name_plural': 'نقش\u200cهای فروشگاه',
            },
        ),
    ]
