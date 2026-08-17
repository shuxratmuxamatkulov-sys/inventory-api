from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Category, Product, Transaction
from .serializers import CategorySerializer, ProductSerializer, TransactionSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # JWT tekshiruvini ushbu view uchun to'liq o'chirish

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # JWT tekshiruvini ushbu view uchun to'liq o'chirish

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer