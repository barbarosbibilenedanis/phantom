from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from order.models import *
from tenant.models import *


class Category(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="categories", verbose_name="Şirket")
    name = models.CharField(max_length=255, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    image = models.ImageField(blank=False,null=False)
    activate = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        unique_together = ('slug', 'tenant')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

class Product(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="products", verbose_name="Şirket")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Kategori")
    name = models.CharField(max_length=255, verbose_name="Ürün Adı")
    description = models.TextField(null=True, blank=True, verbose_name="Ürün Açıklaması")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")
    stock = models.PositiveIntegerField(verbose_name="Stok Miktarı",default=999)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    image = models.ImageField(blank=False,null=False)
    activate = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        unique_together = ('slug', 'tenant')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"category_slug": self.category.slug, "product_slug": self.slug})
