from django.db import models
from django.contrib.auth.models import AbstractUser

# المستخدم المخصص
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="الهاتف")
    ROLE_CHOICES = [
        ('admin', 'مشرف'),
        ('manager', 'مدير'),
        ('cashier', 'كاشير'),
        ('chef', 'شيف'),
        ('delivery', 'مندوب'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='cashier', verbose_name="الدور")

    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"

    def __str__(self):
        return self.username

# العملاء
class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name="الاسم")
    phone = models.CharField(max_length=20, unique=True, verbose_name="الهاتف")
    email = models.EmailField(blank=True, null=True, verbose_name="البريد الإلكتروني")
    address = models.TextField(blank=True, null=True, verbose_name="العنوان")
    # الحقل الجديد
    is_blocked = models.BooleanField(default=False, verbose_name="محظور")

    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"

    def __str__(self):
        return self.name

# الأقسام
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم القسم")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")

    class Meta:
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"

    def __str__(self):
        return self.name

# المنتجات
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم المنتج")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="السعر")
    image = models.URLField(blank=True, null=True, verbose_name="صورة")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="القسم")
    stock = models.PositiveIntegerField(default=0, verbose_name="المخزون")
    available = models.BooleanField(default=True, verbose_name="متاح")

    class Meta:
        verbose_name = "وجبة"
        verbose_name_plural = "الوجبات"

    def __str__(self):
        return self.name

# الموظفين
class Employee(models.Model):
    ROLE_CHOICES = [
        ('manager', 'مدير'),
        ('cashier', 'كاشير'),
        ('chef', 'شيف'),
        ('delivery', 'مندوب'),
    ]
    name = models.CharField(max_length=200, verbose_name="الاسم")
    phone = models.CharField(max_length=20, unique=True, verbose_name="الهاتف")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name="الدور")

    class Meta:
        verbose_name = "موظف"
        verbose_name_plural = "الموظفين"

    def __str__(self):
        return f"{self.name} ({self.role})"

# الطلبات
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('preparing', 'قيد التحضير'),
        ('on_the_way', 'في الطريق'),
        ('delivered', 'تم التوصيل'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders", verbose_name="العميل")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="الحالة")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="الإجمالي")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    order_method = models.CharField(max_length=50, choices=[('online','Online'),('offline','Offline')], default='offline')

    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"

    def __str__(self):
        return f"طلب {self.id} - {self.customer.name}"

# تفاصيل الطلب
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="الطلب")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="الوجبة")
    quantity = models.PositiveIntegerField(default=1, verbose_name="الكمية")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="السعر")

    class Meta:
        verbose_name = "عنصر الطلب"
        verbose_name_plural = "عناصر الطلب"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
