from django.db import models
from product.models import *
from tenant.models import *

class Customer(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="customers", verbose_name="Şirket")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="E-posta")
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="İsim")

    def __str__(self):
        return self.name or "Anonim Müşteri"

    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"

class Cart(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="carts", verbose_name="Şirket")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Müşteri")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    session_key = models.CharField(max_length=255, blank=True, null=True)  # Oturum anahtarı
    
    def __str__(self):
        return f"Sepet #{self.id} - {self.customer}"

    def total_price(self):
        return sum(item.total_price() for item in self.cartitem_set.all())

    class Meta:
        verbose_name = "Sepet"
        verbose_name_plural = "Sepetler"

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name="Sepet")
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name="Ürün")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miktar")

    def __str__(self):
        return f"{self.product.name} - {self.quantity} adet"

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Sepet Öğesi"
        verbose_name_plural = "Sepet Öğeleri"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name="Sipariş")
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name="Ürün")
    quantity = models.PositiveIntegerField(verbose_name="Miktar")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")

    def __str__(self):
        return f"Sipariş #{self.order.id} - {self.product.name} - {self.quantity} adet"

    class Meta:
        verbose_name = "Sipariş Öğesi"
        verbose_name_plural = "Sipariş Öğeleri"


class Order(models.Model):
    tenant = models.ForeignKey("tenant.Tenant", on_delete=models.CASCADE, related_name="orders", verbose_name="Şirket")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Müşteri")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Toplam Fiyat")
    shipping_address = models.TextField(verbose_name="Teslimat Adresi")
    table = models.IntegerField(default=1, verbose_name="Masa Numarası")
    comment = models.TextField(blank=True,null=True,default="Açıklama Yok")
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Beklemede'), ('waiting', 'Müşteri Teslim Alması Bekleniyor'), ('delivered', 'Teslim Edildi')],
        default='pending', 
        verbose_name="Durum"
    )

    def __str__(self):
        return f"Sipariş #{self.id} - {self.customer}"

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"

class Message(models.Model):
    tenant = models.ForeignKey("tenant.Tenant", on_delete=models.CASCADE, related_name="messages", verbose_name="Şirket")
    table = models.IntegerField(default = 0)
    isActivate = models.BooleanField(default=True)

    def __str__(self):
        return f"Masa Çağrıyor #{self.tenant} - {self.table}"    