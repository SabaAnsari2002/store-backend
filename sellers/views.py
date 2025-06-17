from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SellerSerializer
from .models import Seller
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def get(self, request):
        try:
            seller = Seller.objects.get(user=request.user)
            serializer = SellerSerializer(seller)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"detail": "شما فروشنده نیستید."}, status=status.HTTP_400_BAD_REQUEST)

class SellerRegister(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SellerLogin(APIView):
    def post(self, request):
        shop_name = request.data.get('shop_name')
        phone = request.data.get('phone')

        try:
            seller = Seller.objects.get(shop_name=shop_name, phone=phone)
            user = seller.user
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"detail": "نام غرفه یا شماره تلفن اشتباه است."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Check_shop(request):
    try:
        seller = Seller.objects.get(user=request.user)
        return Response({'has_shop': True})
    except Seller.DoesNotExist:
        return Response({'has_shop': False})