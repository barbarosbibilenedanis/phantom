# admin.py

from django.contrib import admin
from .models import Category, Product
from order.views import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'tenant')
    search_fields = ('name', 'slug')
    list_filter = ('tenant',)
    prepopulated_fields = {'slug': ('name',)}

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Kullanıcı süper kullanıcı değilse, 'field_to_exclude' alanını formdan çıkar
            form.base_fields.pop('tenant', None)
        return form   


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            # Eğer kullanıcı süper kullanıcı değilse, sadece kendi tenant'ına ait verileri göster
            tenant = get_tenant(request)  # Kullanıcının tenant'ını al
            queryset = queryset.filter(tenant=tenant)
        return queryset
    

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.tenant = get_tenant(request)  # Kullanıcı admin değilse tenant bilgisini ayarlayın
        super().save_model(request, obj, form, change)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'tenant', 'slug')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'tenant')
    prepopulated_fields = {'slug': ('name',)}
    change_form_template = "product_change_form.html"
    exclude = ('stock',)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Kullanıcı süper kullanıcı değilse, 'field_to_exclude' alanını formdan çıkar
            form.base_fields.pop('tenant', None)
        return form   


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            # Eğer kullanıcı süper kullanıcı değilse, sadece kendi tenant'ına ait verileri göster
            tenant = get_tenant(request)  # Kullanıcının tenant'ını al
            queryset = queryset.filter(tenant=tenant)
        return queryset
    

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.tenant = get_tenant(request)  # Kullanıcı admin değilse tenant bilgisini ayarlayın
        super().save_model(request, obj, form, change)

# Kayıtlar
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)


