from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import messages
from django.contrib import admin
from .models import Cart, Order
from .filter import *
from .views import *

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'tenant', 'created_at')
    search_fields = ('customer__name', 'customer__email')
    list_filter = ('tenant', 'created_at')
    

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

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product_name', 'quantity', 'price']
    readonly_fields = ['product_name', 'quantity', 'price']
    extra = 0

    def product_name(self, obj):
        return obj.product.name  # OrderItem modelinde 'product' ilişkisi olduğu varsayılıyor.

    product_name.short_description = 'Ürün İsmi'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'order_items_names', 'total_price', 'status', 'tenant', 'created_at')
    search_fields = ('customer__name', 'customer__email', 'shipping_address')
    list_filter = ('table','status', 'tenant', 'created_at')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    def order_items_names(self, obj):
        return ", ".join([item.product.name for item in obj.orderitem_set.all()])
    order_items_names.short_description = 'Sipariş Kalemleri'
    
    def changelist_view(self, request, extra_context=None):
        # Tablo numaralarını almak için queryset'i kullanabilirsiniz
        tenant = get_tenant(request)
        orders = Order.objects.filter(tenant=tenant,status='pending')
        tables = set(orders.values_list('table', flat=True))
        
        if extra_context is None:
            extra_context = {}

        # Tablo bilgilerini tutmak için bir liste oluşturuyoruz
        extra_context['tables'] = []

        for i in tables:
            message_exists = Message.objects.filter(tenant=tenant, isActivate=True).exists()
            if message_exists:
                extra_context['tables'].append({"name": i, "color": "red"})  # Tablo numaralarını şablona geçiyoruz
            else:
                extra_context['tables'].append({"name": i, "color": "blue"})

        return super().changelist_view(request, extra_context=extra_context)


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
    
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('product__name', 'cart__customer__name')
    list_filter = ('cart__tenant',)
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

admin.site.register(Message)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('product__name', 'order__customer__name')
    list_filter = ('order__tenant',)
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

