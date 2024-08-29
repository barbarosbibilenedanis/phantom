from django.db import models
from django.contrib.auth.models import AbstractUser

class Tenant(models.Model):
    name = models.CharField(max_length=255, verbose_name="Şirket Adı")
    hostname = models.CharField(max_length=255, unique=True, verbose_name="Hostname")
    address = models.TextField(verbose_name="Adres")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(verbose_name="E-posta")
    about = models.TextField(verbose_name="Hakkımızda")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    logo = models.ImageField(verbose_name="Logo",blank=True,null=True)
    slider = models.ImageField(verbose_name="AnaSayfa Resmi",blank=True,null=True)
    home_page = models.CharField(verbose_name = "Slider Açıklama",max_length = 200)
    menu_slider = models.ImageField(verbose_name="Menu Arkaplan Resmi",blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Şirket"
        verbose_name_plural = "Şirketler"

class ToslaSetting(models.Model):
    api_key = models.CharField(max_length=500, verbose_name="Api Pass")
    secret_key = models.CharField(max_length=500, verbose_name="Base URL")
    base_url = models.CharField(max_length=500, verbose_name="Api User")
    key_url = models.CharField(max_length=500, verbose_name="Client ID")

    def __str__(self):
        return self.secret_key

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Şirket")

