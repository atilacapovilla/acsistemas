from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import datetime

class Tipo(models.Model):
    nome = models.CharField(max_length=50)
    ordem = models.IntegerField(null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    class Meta:
        ordering = ['ordem', 'nome']

class Grupo(models.Model):
    TIPO_GRUPO_CHOICE = (
        ('E', 'Entrada'),
        ('I', 'Investimento'),
        ('S', 'Saida'),
        ('T', 'Tranferencia'),
    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=TIPO_GRUPO_CHOICE, default='S')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    
    def total_planejamento_grupo(self):
        valores = Categoria.objects.filter(grupo__id = self.id).aggregate(Sum('valor_planejamento'))
        return valores['valor_planejamento__sum'] if valores['valor_planejamento__sum'] else 0
    
    def total_gasto_grupo(self):
        valores = Movimento.objects.filter(
            categoria__grupo__id = self.id).filter(
                data_pagamento__year=datetime.now().year, 
                data_pagamento__month=datetime.now().month).aggregate(Sum('valor'))
        return valores['valor__sum'] if valores['valor__sum'] else 0
    
    class Meta:
        ordering = ['tipo', 'nome']

class Categoria(models.Model):
    TIPO_CATEGORIA_CHOICE = (
        ('FX', 'Fixa'),
        ('VR', 'Variavel'),
        ('TR', 'Tranferencia'),
        ('RD', 'Rendimentos'),
    )

    tipo = models.CharField(max_length=2, choices=TIPO_CATEGORIA_CHOICE, default='VR')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='grupos')
    nome = models.CharField(max_length=50)
    valor_planejamento = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nome}'
    
    def total_gasto(self):
        valores = Movimento.objects.filter(
            categoria__id = self.id).filter(
                data_pagamento__year=datetime.now().year, 
                data_pagamento__month=datetime.now().month).aggregate(Sum('valor'))
        return valores['valor__sum'] if valores['valor__sum'] else 0
    
    def calcula_percentual_gasto_por_categoria(self):
        total_gasto = self.total_gasto()
        if total_gasto == 0 or self.valor_planejamento == 0:
            percentual = 0
        else:
            percentual =  (total_gasto * 100) / self.valor_planejamento 
        return percentual
    
    class Meta:
        ordering = ['nome']

class Conta(models.Model):
    TIPO_CONTA_CHOICE = (
        ('CC', 'Conta Corrente'),
        ('DN', 'Dinheiro'),
        ('CT', 'Cartão Crédito'),
        ('IN', 'Investimentos')
    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=TIPO_CONTA_CHOICE, default='CC')
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    saldo_atual = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']


class Pessoa(models.Model):
    nome = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']

class Movimento(models.Model):
    TIPO_MOVIMENTO_CHOICE = (
        ('D', 'Despesa'),
        ('R', 'Receita'),
    )
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='categorias')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=50, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=1, choices=TIPO_MOVIMENTO_CHOICE, default='D')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.descricao} - {self.data_vencimento} - {self.data_pagamento} - {self.valor}'
    
    class Meta:
        ordering = ['-data_vencimento', 'data_pagamento', 'tipo']
