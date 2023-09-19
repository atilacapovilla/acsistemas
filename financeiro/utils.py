from datetime import date
from django.db.models import Q
from django.db.models import Sum

from .models import Conta, Movimento

today = date.today()

def atualiza_saldo(usuario):
    saldo_total = 0
    despesas = 0
    receitas = 0

    contas = Conta.objects.filter(Q(usuario=usuario), Q(tipo='CC') | Q(tipo='DN'),)
    for conta in contas:
        transacoes = Movimento.objects.filter(conta=conta).exclude(data_pagamento=None)
        despesas = transacoes.filter(tipo='D').aggregate(Sum('valor'))['valor__sum']
        if despesas == None:
            despesas = 0
        receitas = transacoes.filter(tipo='R').aggregate(Sum('valor'))['valor__sum']
        if receitas == None:
            receitas = 0
        saldo = conta.saldo_inicial + (receitas or 0) - (despesas or 0)
        conta.saldo_atual = saldo
        conta.save()
        saldo_total += saldo

    
    contas_outras = Conta.objects.filter(usuario=usuario).exclude(tipo='CC').exclude(tipo='DN').order_by('tipo')
    for conta in contas_outras:
        transacoes = Movimento.objects.filter(conta=conta)
        despesas = transacoes.filter(tipo='D').aggregate(Sum('valor'))['valor__sum']
        if despesas == None:
            despesas = 0
        receitas = transacoes.filter(tipo='R').aggregate(Sum('valor'))['valor__sum']
        if receitas == None:
            receitas = 0
        saldo = conta.saldo_inicial + (receitas or 0) - (despesas or 0)
        conta.saldo_atual = saldo
        conta.save()
        
    return contas, saldo_total, contas_outras

def calcula_balanco(usuario, ano, mes):
    transacoes = Movimento.objects\
        .filter(usuario=usuario, data_pagamento__year=ano, data_pagamento__month=mes)
    despesas = transacoes.filter(tipo='D').exclude(categoria__tipo='TR').aggregate(Sum('valor'))['valor__sum']
    if despesas == None:
        despesas = 0
    receitas = transacoes.filter(tipo='R').exclude(categoria__tipo='TR').aggregate(Sum('valor'))['valor__sum']
    if receitas == None:
        receitas = 0
    balanco = receitas - despesas

    return receitas, despesas, balanco

def calcula_pendentes(saldo_total, usuario):
    despesas_fluxo = Movimento.objects.filter(
        usuario=usuario,
        tipo='D',
        data_vencimento__year=today.year, 
        data_vencimento__month=today.month, 
        data_pagamento=None
        ).order_by('data_vencimento')
    receitas_fluxo = Movimento.objects.filter(
        usuario=usuario,
        tipo='R',
        data_vencimento__year=today.year, 
        data_vencimento__month=today.month, 
        data_pagamento=None
        ).order_by('data_vencimento')
    despesas_vencer = despesas_fluxo.aggregate(Sum('valor'))['valor__sum']
    if despesas_vencer == None:
        despesas_vencer = 0
    receitas_vencer = receitas_fluxo.aggregate(Sum('valor'))['valor__sum']
    if receitas_vencer == None:
        receitas_vencer = 0
    saldo_pendentes = saldo_total + (receitas_vencer or 0) - (despesas_vencer or 0)
    return despesas_fluxo, receitas_fluxo, saldo_pendentes

def calcula_vencidos_não_pagos(usuario):
    vencidos = Movimento.objects.filter(
        usuario=usuario,
        data_vencimento__lte=today, 
        data_pagamento=None)
    return vencidos


def baixa_cartoes(usuario, data_pagamento, conta_debito, categoria, pessoa , conta_id , data_vencimento):
    cartoes = Movimento.objects.filter(
        usuario=usuario, conta__id=conta_id, data_vencimento=data_vencimento, tipo='D')
    total_cartao = cartoes.aggregate(Sum('valor'))['valor__sum']
   
    for cartao in cartoes:
        cartao.data_pagamento = data_pagamento
        cartao.save()

    movimento = Movimento(
                data_vencimento=data_pagamento,
                data_pagamento=data_pagamento,
                conta_id=conta_debito,
                categoria_id=categoria,
                pessoa_id=pessoa,
                valor=total_cartao,
                tipo='D',
                usuario=usuario,
            )
    movimento.save()
    movimento = Movimento(
                data_vencimento=data_pagamento,
                data_pagamento=data_pagamento,
                conta_id=conta_id,
                categoria_id=categoria,
                pessoa_id=pessoa,
                valor=total_cartao,
                tipo='R',
                usuario=usuario,
            )
    movimento.save()
        
    return cartoes, total_cartao