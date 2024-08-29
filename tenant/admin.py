from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import User, Tenant, ToslaSetting

admin.site.register(User, UserAdmin)
# Register your models here.
admin.site.register(ToslaSetting)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostname', 'phone', 'email', 'created_at')
    search_fields = ('name', 'hostname', 'email')
    list_filter = ('created_at',)


