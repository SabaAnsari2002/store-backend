from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.db.models import Sum, Count
from datetime import datetime

def dashboard(request):
    monthly_income = 2500000  
    daily_sales = 100000      
    product_visits = 1200    
    new_orders = Order.objects.filter(status='pending').count()

    orders = Order.objects.order_by('-date')[:3]

    monthly_sales = {
        'فروردین': 4200,
        'اردیبهشت': 3200,
        'خرداد': 2000,
        'تیر': 2900,
        'مرداد': 1800,
        'شهریور': 2400,
    }

    context = {
        'monthly_income': monthly_income,
        'daily_sales': daily_sales,
        'product_visits': product_visits,
        'new_orders': new_orders,
        'monthly_sales': monthly_sales,
        'orders': orders,
    }
    return render(request, 'sellerpanel/dashboard.html', context)


def product_list(request):
    products = Product.objects.all()
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST['name'],
            category=request.POST['category'],
            price=request.POST['price'],
            stock=request.POST['stock']
        )
        return redirect('product_list')
    return render(request, 'sellerpanel/product_list.html', {'products': products})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.category = request.POST['category']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.save()
        return redirect('product_list')
    return render(request, 'sellerpanel/edit_product.html', {'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')


def order_list(request):
    orders = Order.objects.all().order_by('-date')
    return render(request, 'sellerpanel/order_list.html', {'orders': orders})


def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('order_list')


def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = request.POST['status']
        order.save()
    return redirect('order_list')


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'sellerpanel/order_detail.html', {'order': order})
