from django.contrib import admin
from .models import Sistema

@admin.register(Sistema)
class SistemaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'url_app', 'icone_app', 'liberado')
    