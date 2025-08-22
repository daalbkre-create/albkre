from rest_framework import viewsets
from .models import Customer, Category, Product, Employee, Order
from .serializers import (
    CustomerSerializer, CategorySerializer, ProductSerializer, EmployeeSerializer,
    OrderReadSerializer, OrderWriteSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all().order_by('id')
    serializer_class = ProductSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('customer').prefetch_related('items__product').all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderReadSerializer
        return OrderWriteSerializer
