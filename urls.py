"""
URL configuration for phantom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from product.views import *
from order.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = "index"),
    path('kategoriler/', category_with_products, name='category_with_products'),
    path('sepete-ekle/', add_to_cart, name='add_to_cart'),
    path('reduce-cart-item/', reduce_cart_item, name='reduce_cart_item'),
    path('plus-cart-item/', plus_cart_item, name='plus_cart_item'),
    path('remove-cart-item/', remove_cart_item, name='remove_cart_item'),
    path('ajax/get-cart/', ajax_get_cart, name='ajax_get_cart'),
    path('checkout/', cart_view, name='checkout'),
     path('about/', about, name='about'),
      path('contact/',contact, name='contact'),
    path('place_order/', place_order, name='place_order'),  # Sipariş işlemi için
    path('order_success/<int:orderid>', order_success, name='order_success'),
    path('order_unsuccess/', order_unsuccess, name='order_unsuccess'),  # Sipariş başarı sayfası
        # Sipariş başarı sayfası
    path('check-messages/', check_messages, name='check_messages'),
    path('update-messages/', update_messages, name='update_messages'),
    path('add-message/', add_message, name='add_message'),
    path('notification/',notification,name='notification'),
    path('messageoffline/', messageoffline, name='messageoffline'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)