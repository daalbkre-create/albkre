from rest_framework import serializers
from .models import Customer, Category, Product, Employee, Order, OrderItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

# لعرض تفاصيل الطلب مع المنتجات
class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderReadSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    items = OrderItemReadSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'total_price', 'created_at', 'items']

# لإنشاء وتعديل الطلبات من التطبيق
class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderWriteSerializer(serializers.ModelSerializer):
    items = OrderItemWriteSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['customer', 'status', 'total_price', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order
