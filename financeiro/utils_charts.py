from django.db.models import Sum
from .models import Movimento

def despesas_variaveis_ano(ano, mes, usuario):
    labels_ano = []
    data_ano = []
    tabela_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',]
    transacoes = Movimento.objects.filter(
        usuario=usuario,
        tipo='D',
        data_pagamento__year=ano,
    )
    transacoes = transacoes.values(
        'data_pagamento__month').annotate(total_despesas=Sum('valor')).order_by('data_pagamento__month')
    
    # teste = transacoes.values(
    #     'categoria__grupo__nome','categoria__nome','data_pagamento__month').annotate(
    #         total_despesas=Sum('valor')).order_by(
    #             'categoria__grupo__nome', 'categoria__nome', 'data_pagamento__month')
    # for t in teste:
    #     print(t['categoria__grupo__nome'],t['categoria__nome'], t['data_pagamento__month'], t['total_despesas'])


    for entry in transacoes:
        mes = entry['data_pagamento__month']
        mes_str = tabela_meses[mes - 1]
        labels_ano.append(mes_str)
        data_ano.append(int(entry['total_despesas']))
    
    return labels_ano, data_ano


def despesas_variaveis_mes(ano, mes, usuario):
    labels = []
    data = []
    
    queryset = Movimento.objects\
        .values('categoria__nome')\
        .annotate(total_despesas=Sum('valor'))\
        .filter(usuario=usuario,tipo='D',data_pagamento__year=ano, data_pagamento__month=mes)\
        .order_by('-total_despesas')
    
    for entry in queryset:
        labels.append(entry['categoria__nome'])
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

