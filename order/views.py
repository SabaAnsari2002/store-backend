from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
from django.db import transaction
from products.models import Product

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).prefetch_related('items')
    
    @action(detail=False, methods=['get'], url_path='by-seller')
    def orders_by_seller(self, request):
        if not hasattr(request.user, 'seller'):
            return Response({'error': 'شما فروشنده نیستید'}, status=403)

        seller = request.user.seller

        orders = Order.objects.filter(
            items__product__seller=seller
        ).distinct().prefetch_related('items__product').order_by('-created_at')

        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart_items = request.data.get('items', [])

        if not cart_items:
            return Response(
                {'error': 'سبد خرید خالی است'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                order = Order.objects.create(user=request.user)
                total_price = 0

                for item in cart_items:
                    product = Product.objects.get(pk=item['product_id'])

                    if product.stock < item['quantity']:
                        return Response(
                            {'error': f'موجودی محصول {product.name} کافی نیست'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    item_total = int(product.price) * int(item['quantity'])
                    total_price += item_total
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=int(product.price),
                        seller=product.seller
                    )
                    # ...
                    order.total_price = int(total_price)
                    order.save()

                order.total_price = total_price
                order.save()

                serializer = self.get_serializer(order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response(
                {'error': 'محصول یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        try:
            order = self.get_queryset().get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'سفارش یافت نشد'}, status=404)
    
        new_status = request.data.get('status')
        if new_status not in ['pending', 'completed', 'cancelled', 'refunded']:
            return Response({'error': 'وضعیت نامعتبر است'}, status=400)
    
        order.status = new_status
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=200)



    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        try:
            order = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            if Order.objects.filter(pk=pk).exists():
                return Response(
                    {"detail": "شما به این سفارش دسترسی ندارید"},
                    status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {"detail": "سفارش مورد نظر یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
            
    def list(self, request):
        orders = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='history')
    def order_history(self, request):
        orders = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)