from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.http import Http404
from tenant.models import *


def index(request):
    tenant = get_tenant(request)
    categories = Category.objects.filter(tenant=tenant, activate = True)
    
    # Her kategori için ürünleri alır ve bir sözlükte saklar
    category_product_map = {}
    for category in categories:
        products = Product.objects.filter(category=category, tenant=tenant, activate = True)
        category_product_map[category] = products
    
    # Template'e kategori ve ürünleri gönderir
    context = {
        'category_product_map': category_product_map,
        'tenant': tenant
    }
    return render(request, 'index.html',context)

def get_tenant(request):
    # Hostname üzerinden tenant'ı alır
    hostname = request.get_host().split(':')[0]  # Port numarasını ayırır
    tenant = get_object_or_404(Tenant, hostname__contains=hostname)
    return tenant


def category_with_products(request):
    # Tenant'ı belirler
    tenant = get_tenant(request)
    
    # Tenant'a bağlı tüm kategorileri alır
    categories = Category.objects.filter(tenant=tenant, activate = True)
    
    # Her kategori için ürünleri alır ve bir sözlükte saklar
    category_product_map = {}
    for category in categories:
        products = Product.objects.filter(category=category, tenant=tenant)
        category_product_map[category] = products
    
    # Template'e kategori ve ürünleri gönderir
    context = {
        'category_product_map': category_product_map,
        'tenant': tenant
    }
    
    return render(request, 'category.html', context)

"""<h1>Kategoriler ve Ürünler</h1>

{% for category, products in category_product_map.items %}
    <h2>{{ category.name }}</h2>
    <ul>
        {% for product in products %}
            <li>{{ product.name }} - {{ product.price }}₺</li>
        {% empty %}
            <li>Bu kategoride henüz ürün yok.</li>
        {% endfor %}
    </ul>
{% endfor %}"""
