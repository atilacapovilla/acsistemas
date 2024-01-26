from django.db.models import Sum
from .models import Movimento

def despesas_mes(ano, mes, usuario):
    labels = []
    data = []
    
    queryset = Movimento.objects\
        .values('categoria__grupo__nome', 'categoria__grupo__tipo')\
        .annotate(total_despesas=Sum('valor'))\
        .filter(usuario=usuario, tipo='D', data_lancamento__year=ano, data_lancamento__month=mes)\
        .exclude(categoria__grupo__tipo='3')\
        .exclude(categoria__grupo__tipo='4')\
        .order_by('-total_despesas')
    
    for entry in queryset:
        labels.append(entry['categoria__grupo__nome'])
        data.append(int(entry['total_despesas']))
    
    return labels, data


def receitas_despesas_ano(ano, usuario):
    labels_ano = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',]
    data_despesas_ano = []
    data_receitas_ano = []
    
    transacoes = Movimento.objects\
        .filter(usuario=usuario,data_lancamento__year=ano,)\
        .exclude(categoria__grupo__tipo='3')\
        .exclude(categoria__grupo__tipo='4')
    
    despesas = transacoes\
        .values('data_lancamento__month')\
        .filter(tipo='D')\
        .annotate(total_despesas=Sum('valor'))\
        .order_by('data_lancamento__month')

    
    receitas = transacoes\
        .values('data_lancamento__month')\
        .filter(tipo='R')\
        .annotate(total_receitas=Sum('valor'))\
        .order_by('data_lancamento__month')
    
    for entry in despesas:
        data_despesas_ano.append(int(entry['total_despesas']))
 
    for entry in receitas:
        data_receitas_ano.append(int(entry['total_receitas']))

    return labels_ano, data_despesas_ano, data_receitas_ano
