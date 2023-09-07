from django.contrib import admin
from .models import Grupo, Categoria, Conta, Pessoa, Movimento

@admin.register(Grupo)
class Grupo(admin.ModelAdmin):
    list_display = ('nome','tipo', 'grupo')
    
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'essencial', 'usuario')
    
@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'saldo_inicial', 'usuario', 'logo')
 
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario')

@admin.register(Movimento)
class MovimentoAdmin(admin.ModelAdmin):
    list_display = ('data_vencimento', 'data_pagamento', 'conta', 'descricao', 'valor', 'tipo', 'usuario')