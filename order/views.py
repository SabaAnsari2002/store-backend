from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
from django.db import transaction
from products.models import Product
from rest_framework.views import APIView




class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print("User ID:", self.request.user.id)
        return Order.objects.filter(user=self.request.user)


    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart_items = request.data.get('items', [])
        if not cart_items:
            return Response({'error': 'سبد خرید خالی است'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                order = Order.objects.create(user=request.user)
                total_price = 0

                for item in cart_items:
                    product = Product.objects.get(pk=item['product_id'])

                    if product.stock < item['quantity']:
                        raise Exception(f"موجودی محصول {product.name} کافی نیست")

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=product.price,
                        seller=product.seller
                    )

                    product.stock -= item['quantity']
                    product.save()

                    total_price += product.price * item['quantity']

                order.total_price = total_price
                order.save()

                serializer = self.get_serializer(order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({'error': 'محصول یافت نشد'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    @action(detail=False, methods=['get'], url_path='history')
    def order_history(self, request):
        orders = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        try:
            order = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            if Order.objects.filter(pk=pk).exists():
                return Response({"detail": "شما به این سفارش دسترسی ندارید"}, status=403)
            return Response({"detail": "سفارش یافت نشد"}, status=404)

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        try:
            order = self.get_queryset().get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'سفارش یافت نشد'}, status=404)

        new_status = request.data.get('status')
        if new_status not in ['pending', 'completed', 'cancelled']:
            return Response({'error': 'وضعیت نامعتبر است'}, status=400)

        order.status = new_status
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
