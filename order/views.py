from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from product.views import get_tenant
from django.contrib import messages
from django.utils import timezone
import hashlib
import base64
import random
from datetime import datetime
import requests
from product.models import *
from tenant.models import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        # Mevcut tenant'ı alır
        tenant = get_tenant(request)
        
        # Ürünü alır
        product = get_object_or_404(Product, id=product_id, tenant=tenant)
        
        # Sepeti alır veya oluşturur
        cart = get_cart(request)
        
        # Sepetteki ürünü alır veya oluşturur
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Ürün zaten sepette varsa, miktarı günceller
            cart_item.quantity += quantity
            cart_item.save()
        
        # Sepet toplam fiyatını hesaplar
        total_price = cart.total_price()
        item_count = cart.cartitem_set.count()
        
        # JSON yanıtı döner
        return JsonResponse({
            'cart_item_count': item_count,
            'cart_total_price': total_price,
        })
    return JsonResponse({'error': 'Geçersiz istek'}, status=400)

"""<!-- Sepetteki ürün sayısını göstermek için bir yer -->
<div>
    Sepetteki ürün sayısı: <span id="cart-count">0</span>
    Toplam fiyat: <span id="cart-total">0₺</span>
</div>

<!-- Ürün ekleme butonu örneği -->
<button onclick="addToCart(1, 1)">Ürünü Sepete Ekle</button>
"""

def get_cart(request):
    tenant = get_tenant(request)
    session_key = request.session.session_key
    
    if not session_key:
        request.session.create()  # Oturum anahtarını oluşturur
    
    cart, created = Cart.objects.get_or_create(
        tenant=tenant,
        customer=None,  # Giriş yapmamış kullanıcılar için
        session_key=session_key
    )
    return cart

def ajax_get_cart(request):
    cart = get_cart(request)
    cart_items = cart.cartitem_set.select_related('product').all()
    
    items_data = []
    for item in cart_items:
        items_data.append({
            'id' : item.pk,
            'name': item.product.name,
            'price': str(item.product.price),
            'quantity': item.quantity,
            'total_price': str(item.product.price * item.quantity),
            'image': "/"+str(item.product.image)
        })

    response_data = {
        'items': items_data,
        'total_price': str(cart.total_price()),
        'item_count': cart_items.count(),
    }
    
    return JsonResponse(response_data)

def cart_view(request):
    cart = get_cart(request)
    cart_items = cart.cartitem_set.select_related('product').all()  # Sepetteki ürünleri al
    tenant = get_tenant(request)
    
    return render(request, 'checkout.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.total_price(),
        'item_count': cart_items.count(),
        'tenant': tenant
    })


def reduce_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        tenant = get_tenant(request)  # Tenant'ı alır

        # Sepetteki ürünü bulur
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__tenant=tenant)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()  # Miktar 1 ise ürünü sepetten siler
            return JsonResponse({'status': 'success'})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Ürün bulunamadı'}, status=404)

    return JsonResponse({'error': 'Geçersiz istek'}, status=400)


def plus_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        tenant = get_tenant(request)  # Tenant'ı alır

        # Sepetteki ürünü bulur
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__tenant=tenant)
            if cart_item.quantity > 0:
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item.delete()  # Miktar 1 ise ürünü sepetten siler
            return JsonResponse({'status': 'success'})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Ürün bulunamadı'}, status=404)

    return JsonResponse({'error': 'Geçersiz istek'}, status=400)


def remove_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        tenant = get_tenant(request)  # Tenant'ı alır

        # Sepetteki ürünü bulur ve siler
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__tenant=tenant)
            cart_item.delete()
            return JsonResponse({'status': 'success'})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Ürün bulunamadı'}, status=404)

    return JsonResponse({'error': 'Geçersiz istek'}, status=400)
toslaSetting = ToslaSetting.objects.first()

API_PASS = toslaSetting.api_key
CLIENT_ID = toslaSetting.key_url
API_USER = toslaSetting.base_url
BASE_URL = toslaSetting.secret_key



def generate_hash(api_pass, client_id, api_user, rnd, time_span):
    hash_string = f"{api_pass}{client_id}{api_user}{rnd}{time_span}"
    sha512 = hashlib.sha512()
    sha512.update(hash_string.encode('utf-8'))
    hash_bytes = sha512.digest()
    return base64.b64encode(hash_bytes).decode('utf-8')

def start_three_d_payment(url,money,id):
    API_PASS = toslaSetting.api_key
    CLIENT_ID = toslaSetting.key_url
    API_USER = toslaSetting.base_url
    BASE_URL = toslaSetting.secret_key
    rnd = str(random.randint(1, 1000000))
    time_span = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_value = generate_hash(API_PASS, CLIENT_ID, API_USER, rnd, time_span)
    request_data = {
        "ClientId": CLIENT_ID,
        "ApiUser": API_USER,
        "Rnd": rnd,
        "TimeSpan": time_span,
        "Hash": hash_value,
        "CallbackUrl": "https://"+url+"/order_success/{0}".format(id),
        "OrderId":"Bibilen{0}".format(str(id)),
        "Amount": int(money * 100),  # Ödeme Tutarı (örneğin: 10.00 TL)
        "Currency": 949,

    }
    print(request_data)

    response = requests.post(f"{BASE_URL}threeDPayment", json=request_data)

    response_data = response.json()
    return response_data.get("ThreeDSessionId")
def process_card_form(three_d_session_id,card):
    card_data = {
        "ThreeDSessionId": three_d_session_id,
        "CardHolderName": card["card_name"],
        "CardNo": card["card_number"],
        "ExpireDate": card["card_expiry"],
        "Cvv": str(card["card_cvc"])
    }
    print(card_data)

    response = requests.post(f"{BASE_URL}ProcessCardForm", data=card_data)
    
    return response.text  # Başarı kodu

def complete_payment(price,pk):
    rnd = str(random.randint(1, 1000000))
    time_span = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_value = generate_hash(API_PASS, CLIENT_ID, API_USER, rnd, time_span)
    if price <= 0:
        return redirect('category_with_products')  # Başarı sayfasına yönlendir

    request_data = {
        "ClientId": CLIENT_ID,
        "ApiUser": API_USER,
        "Rnd": rnd,
        "TimeSpan": time_span,
        "Hash": hash_value,
        "OrderId":"Bibilen" + str(pk),
        "Amount": int(price * 100),  # Ödeme Tutarı (örneğin: 10.00 TL)
        "Currency": 949  # Para birimi (TL)
    }
    response = requests.post(f"{BASE_URL}inquiry", json=request_data)
    print(2,request_data)
    response_data = response.json()
    print(3,response_data)
    return (response_data.get("Code") == 0  and response_data.get("BankResponseCode") == "00")


def checkout(request):
    if request.method == 'POST':
        cart = get_cart(request)
        
        if not cart or not cart.cartitem_set.exists():
            messages.error(request, 'Sepetiniz boş.')
            return redirect('index')  # Hata sayfasına yönlendir
        
        
        comment = request.COOKIES.get('comment', 'Yorum Yok')
        order = Order.objects.create(
            customer=None,  # Üye olmayan kullanıcılar için
            tenant=cart.tenant,
            total_price=cart.total_price(),
            shipping_address = "Cafe - Ofis",
            status='pending',
            created_at=timezone.now(),
            comment = comment
        )

        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                shipping_address = "Cafe - Ofis",
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                tenant = cart.tenant,
                comment = comment
            )
            
      
        cart.cartitem_set.all().delete()
        cart.delete()
        messages.success(request, 'Siparişiniz başarıyla oluşturuldu!')
        return redirect('order_success')  # Başarı sayfasına yönlendir

    return redirect('some_page')  # Hata sayfasına yönlendir
"""
<form method="post" action="{% url 'checkout' %}">
    {% csrf_token %}
    <button type="submit">Siparişi Tamamla</button>
</form>
"""


def place_order(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_number')
        card_number = request.POST.get('card_number')
        card_expiry = request.POST.get('card_expiry')
        card_cvc = request.POST.get('card_cvc')
        card_name = request.POST.get('card_name').split(' ')  
        card = {
        'table_name': table_name,
        'card_number': card_number,
        'card_expiry': card_expiry,
        'card_cvc': card_cvc,
        'card_name': card_name
    }

        cart = get_cart(request)
        tenant = get_tenant(request)

        if not cart or not cart.cartitem_set.exists():
            messages.error(request, 'Sepetiniz boş.')
            return redirect('category_with_products')
        else:
            three_d_session_id = start_three_d_payment(request.get_host(),cart.total_price(),cart.pk)

            if not three_d_session_id:
                print("ThreeDSessionId alınamadı.")
                return HttpResponse()


            data = process_card_form(three_d_session_id,card)
            return HttpResponse(data)

    return redirect('')
@csrf_exempt
def order_success(request,orderid):
    tenant = get_tenant(request)
    cart = get_object_or_404(Cart, pk=orderid)
    context = {
        'tenant': tenant
    }
    if  complete_payment(cart.total_price(),cart.pk) == True:
        order = Order.objects.create(
            customer=None,  # Üye olmayan kullanıcılar için
            tenant=cart.tenant,
            total_price=cart.total_price(),
            status='Pending',
            table = int(request.COOKIES.get('table', 0)),
            created_at=timezone.now()
        )

        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        cart.cartitem_set.all().delete()
        cart.delete()
        return render(request, 'order_success.html',context)
    else: 
        return render(request, 'order_unsuccess.html',context)
        


def contact(request):
    tenant = get_tenant(request)
    context = {
        'tenant': tenant
    }
    return render(request, 'contact.html',context)
        
def about(request):
    tenant = get_tenant(request)
    context = {
        'tenant': tenant
    }
    return render(request, 'about.html',context)

def order_unsuccess(request):
    tenant = get_tenant(request)
    context = {
        'tenant': tenant
    }
    return render(request, 'order_unsucces.html',context)

def message(request):
    tenant = get_tenant(request)
    messages = Message.objects.filter(isActivate=True, tenant=tenant)

    message_list = list(messages.values('table', 'isActivate'))  # Örneğin sadece 'table' ve 'isActivate' alanlarını döndürüyoruz

    context = {
        'messages': message_list
    }

    return JsonResponse(context)

def check_messages(request):
    tenant = get_tenant(request)
    messages = Message.objects.filter(isActivate=True, tenant=tenant)

    message_list = list(messages.values('id', 'table'))  # ID ve table alanlarını döndürüyoruz

    return JsonResponse({'messages': message_list})

@csrf_exempt
def update_messages(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('action') == 'deactivate':
            Message.objects.filter(isActivate=True).update(isActivate=False)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})
@csrf_exempt
def messageoffline(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        table_number = data.get('table')
        tenant = get_tenant(request)
        Message.objects.filter(table=table_number, tenant=tenant, isActivate=True).update(isActivate=False)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def add_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        table_number = data.get('table')
        tenant = get_tenant(request)
        Message.objects.create(table=table_number, tenant=tenant, isActivate=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def notification(request):
    if request.method == 'POST':
        session_key = request.session.session_key
        data = json.loads(request.body)
        table = int(request.COOKIES.get('table', 0))
        if session_key:
            tenant = get_tenant(request)
            # Siparişin varlığını kontrol et
            order_exists = Order.objects.filter(table=table,status="waiting", tenant=tenant).exists()
        
            if order_exists:
                return JsonResponse({'message': 'Ürününüz hazır, kasadan bekleniyorsunuz!'})
            else:
                return JsonResponse({'message': 'Bekleyen sipariş bulunamadı.'})
        
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})