from django.contrib import admin
from .models import (File, Client)

@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','auth_token','is_verified','created_at']

@admin.register(File)
class FileModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'file']