# backend/admin.py
# لا تسجل أي موديل هنا لتجنب AlreadyRegistered
# يمكنك فقط تخصيص شعار/CSS عام إذا أحببت

from django.contrib import admin
from django.utils.html import format_html

# شعار ولوحة الإدارة العامة
admin.site.site_header = format_html('<img src="/static/logo.png" style="height:50px;"> لوحة تحكم مطعمك')
admin.site.site_title = "لوحة تحكم مطعمك"
admin.site.index_title = "مرحباً بك في لوحة التحكم"

# CSS مخصص
class CustomAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ("/static/admin/css/style.css",)}
