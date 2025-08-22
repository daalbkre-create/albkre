from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Customer, Category, Product, Employee, Order, OrderItem

# ====================================
# شعار ولوحة الإدارة العامة
# ====================================
admin.site.site_header = format_html('<img src="/static/logo.png" style="height:50px;"> لوحة تحكم مطعمك')
admin.site.site_title = "لوحة تحكم مطعمك"
admin.site.index_title = "مرحباً بك في لوحة التحكم"

# ====================================
# UserAdmin لتعديل وإضافة المدراء
# ====================================
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('معلومات شخصية', {'fields': ('first_name', 'last_name', 'email', 'phone', 'role')}),
        ('صلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('التواريخ', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'role', 'is_staff', 'is_superuser', 'is_active')
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

# تسجيل UserAdmin مرة واحدة فقط
try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass

# ====================================
# Inline لعرض تفاصيل الطلب داخل الطلب
# ====================================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

# ====================================
# CustomAdmin لجميع الموديلات الأخرى
# ====================================
class CustomAdmin(admin.ModelAdmin):
    list_per_page = 20
    class Media:
        css = {
            "all": ("/static/admin/css/style.css",)
        }

# ====================================
# تسجيل الموديلات الأخرى
# ====================================
@admin.register(Product)
class ProductAdmin(CustomAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    search_fields = ('name',)
    list_filter = ('category', 'available')
    actions = ['mark_as_available', 'mark_as_unavailable']

    def mark_as_available(self, request, queryset):
        queryset.update(available=True)
        self.message_user(request, "تم تفعيل المنتجات المحددة.")
    mark_as_available.short_description = "تفعيل المنتجات المحددة"

    def mark_as_unavailable(self, request, queryset):
        queryset.update(available=False)
        self.message_user(request, "تم تعطيل المنتجات المحددة.")
    mark_as_unavailable.short_description = "تعطيل المنتجات المحددة"

@admin.register(Category)
class CategoryAdmin(CustomAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(CustomAdmin):
    list_display = ('name', 'phone', 'email', 'is_blocked')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('is_blocked',)

@admin.register(Employee)
class EmployeeAdmin(CustomAdmin):
    list_display = ('name', 'phone', 'role')
    list_filter = ('role',)
    search_fields = ('name', 'phone')

@admin.register(Order)
class OrderAdmin(CustomAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__name',)
    inlines = [OrderItemInline]
    readonly_fields = ('id', 'customer', 'order_method', 'created_at', 'total_price')
    fieldsets = (
        (None, {
            'fields': ('id', 'customer', 'order_method', 'created_at', 'status', 'total_price')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(CustomAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('product__name', 'order__id')
