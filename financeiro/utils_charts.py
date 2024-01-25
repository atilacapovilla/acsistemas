from django.db.models import Sum
from .models import Movimento

def despesas_ano(ano, mes, usuario):
    labels_ano = []
    data_ano = []
    tabela_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',]
    transacoes = Movimento.objects\
        .filter(usuario=usuario,tipo='D', data_lancamento__year=ano,)\
        .exclude(categoria__grupo__tipo='3')\
        .exclude(categoria__grupo__tipo='4')
        
    transacoes = transacoes\
        .values('data_lancamento__month')\
        .annotate(total_despesas=Sum('valor'))\
        .order_by('data_lancamento__month')
    

    for entry in transacoes:
        mes = entry['data_lancamento__month']
        mes_str = tabela_meses[mes - 1]
        labels_ano.append(mes_str)
        data_ano.append(int(entry['total_despesas']))
    
    return labels_ano, data_ano


def despesas_mes(ano, mes, usuario):
    labels = []
    data = []
    
    queryset = Movimento.objects\
        .values('categoria__grupo__nome', 'categoria__grupo__tipo')\
        .annotate(total_despesas=Sum('valor'))\
        .filter(usuario=usuario,tipo='D',data_lancamento__year=ano, data_lancamento__month=mes)\
        .exclude(categoria__grupo__tipo='3')\
        .exclude(categoria__grupo__tipo='4')\
        .order_by('-total_despesas')
    
    for entry in queryset:
        labels.append(entry['categoria__grupo__nome'])
        data.append(int(entry['total_despesas']))
    
    return labels, data


def despesas_categoria_ano(ano, mes, categoria_id, usuario):
    labels_ano = []
    data_ano = []
    tabela_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',]
    transacoes = Movimento.objects.filter(
        usuario=usuario,
        categoria=categoria_id,
        data_pagamento__year=ano,
    )

    transacoes = transacoes.values(
        'data_pagamento__month').annotate(total_despesas=Sum('valor')).order_by('data_pagamento__month')
    
    
    for entry in transacoes:
        mes = entry['data_pagamento__month']
        mes_str = tabela_meses[mes - 1]
        labels_ano.append(mes_str)
        data_ano.append(int(entry['total_despesas']))
    
    return labels_ano, data_ano

def despesas_pessoas_categoria_ano(ano, mes, categoria_id, usuario):
    labels = []
    data = []
    transacoes = Movimento.objects.filter(
        usuario=usuario,
        categoria=categoria_id,
        data_pagamento__year=ano,
        data_pagamento__month=mes,
    )
    transacoes = transacoes.values(
        'pessoa__nome').annotate(total_despesas=Sum('valor')).order_by('-total_despesas')
    
    for entry in transacoes:
        labels.append(entry['pessoa__nome'])
        data.append(int(entry['total_despesas']))
    
    return labels, data

