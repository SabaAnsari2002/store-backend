from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, DiscountSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import Ticket,Discount, Address, BankCard, CustomUser
from .serializers import TicketSerializer, TicketReplySerializer, AddressSerializer, BankCardSerializer,UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied

class TicketPagination(PageNumberPagination):
    page_size = 10 

class TicketListCreateView(generics.ListCreateAPIView):
    pagination_class = TicketPagination
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Ticket.objects.none()
            
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("کاربر احراز هویت نشده است")
            
        serializer.save(user=self.request.user)

class TicketReplyCreateView(generics.CreateAPIView):
    serializer_class = TicketReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        ticket = generics.get_object_or_404(Ticket, id=ticket_id)


        if self.request.user.is_staff and ticket.status != 'answered':
            ticket.status = 'answered'
            ticket.save()

        is_staff_reply = True if self.request.user.is_staff else False
        serializer.save(ticket=ticket, user=self.request.user, is_staff_reply=is_staff_reply)


class AdminTicketUpdateView(generics.UpdateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Ticket.objects.all()
    
    def perform_update(self, serializer):
        if 'status' not in serializer.validated_data:
            serializer.validated_data['status'] = self.get_object().status
        serializer.save()
        
        
class TicketRetrieveView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=self.request.user)

class BankCardListCreateView(generics.ListCreateAPIView):
    serializer_class = BankCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BankCard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BankCardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BankCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BankCard.objects.filter(user=self.request.user)
        
class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if not Address.objects.filter(user=self.request.user).exists():
            serializer.save(user=self.request.user, is_default=True)
        else:
            serializer.save(user=self.request.user)

class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

class SetDefaultAddressView(generics.UpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        Address.objects.filter(user=self.request.user).update(is_default=False)
        serializer.save(is_default=True)
        

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "phone": request.user.phone,
            "date_joined": request.user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterUser(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            phone = serializer.validated_data.get('phone')
            
            if CustomUser.objects.filter(email=email).exists():
                return Response(
                    {'email': ['این ایمیل قبلاً ثبت شده است.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if CustomUser.objects.filter(phone=phone).exists():
                return Response(
                    {'phone': ['این شماره تلفن قبلاً ثبت شده است.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = self.perform_create(serializer)
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)             
            
            return Response({
                'user': serializer.data,
                'user_id': user.id,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save()


class CheckDuplicatesView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip()
        phone = request.data.get('phone', '').strip()
        
        response_data = {
            'email_exists': False,
            'phone_exists': False,
            'errors': {}
        }
        
        if email:
            if CustomUser.objects.filter(email=email).exists():
                response_data['email_exists'] = True
                response_data['errors']['email'] = ['این ایمیل قبلاً ثبت شده است.']
        
        if phone:
            if CustomUser.objects.filter(phone=phone).exists():
                response_data['phone_exists'] = True
                response_data['errors']['phone'] = ['این شماره تلفن قبلاً ثبت شده است.']
        
        return Response(response_data, status=status.HTTP_200_OK)

class DiscountViewSet(viewsets.ModelViewSet):
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Discount.objects.all()
        
        if not self.request.user.is_staff:
            if hasattr(self.request.user, 'seller'):
                queryset = queryset.filter(seller=self.request.user.seller)
            else:
                queryset = queryset.none()
                
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'seller'):
            serializer.save(seller=self.request.user.seller)
        else:
            serializer.save()
            
            
class ActiveDiscountsView(generics.ListAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Discount.objects.filter(is_active=True)
