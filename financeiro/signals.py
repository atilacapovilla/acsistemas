# from datetime import date
# from django.db.models.signals import pre_save, post_save
# from django.db.models import Sum
# from django.dispatch import receiver
# from financeiro.models import Movimento, Conta, ContaSaldo


# @receiver(pre_save, sender=Movimento)
# def movimento_pre_save(sender, instance,  **kwargs):
#     print('##### pre save #####')
#     print(instance.valor)
#     global valor_anterior
#     valor_anterior = instance.valor

# @receiver(post_save, sender=Movimento)
# def movimento_post_save(sender, instance, created, **kwargs):
#     today = date.today()
#     contas = Conta.objects.filter(usuario=instance.usuario).order_by('nome')
#     for conta in contas:
#         transacoes = Movimento.objects.filter(conta=conta, data_pagamento__year=today.year, data_pagamento__month=today.month)
#         despesas = transacoes.filter(tipo='D').aggregate(Sum('valor'))['valor__sum']
#         if despesas == None:
#             despesas = 0
#         receitas = transacoes.filter(tipo='R').aggregate(Sum('valor'))['valor__sum']
#         if receitas == None:
#             receitas = 0
#         saldo = conta.saldo_inicial + (receitas or 0) - (despesas or 0)

#         obj, created = ContaSaldo.objects.update_or_create(
#             saldo_inicial = conta.saldo_inicial,
#             despesas = despesas,
#             receitas = receitas,
#             saldo_final = saldo,
#             defaults={"conta": conta},
#         )

