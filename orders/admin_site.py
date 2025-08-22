from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product, Category

# إنشاء AdminSite مخصص
class AlbkreAdminSite(admin.AdminSite):
    site_header = "إدارة منتجات البكري"       # رأس الصفحة
    site_title = "البكري Admin"              # عنوان التبويب
    index_title = "لوحة تحكم إدارة المنتجات"  # عنوان الصفحة الرئيسية

# تسجيل الموقع الجديد
admin_site = AlbkreAdminSite(name='albkre_admin')


# إدارة المنتجات
@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    search_fields = ('name',)
    list_filter = ('category', 'available')
    actions = ['mark_as_available', 'mark_as_unavailable']

    # إجراءات مخصصة
    def mark_as_available(self, request, queryset):
        queryset.update(available=True)
        self.message_user(request, "تم تفعيل المنتجات المحددة.")
    mark_as_available.short_description = "تفعيل المنتجات المحددة"

    def mark_as_unavailable(self, request, queryset):
        queryset.update(available=False)
        self.message_user(request, "تم تعطيل المنتجات المحددة.")
    mark_as_unavailable.short_description = "تعطيل المنتجات المحددة"


# إدارة الفئات
@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
