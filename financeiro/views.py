import json
from datetime import date
from calendar import monthrange
from typing import Any


from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Sum
from django.db.models import ProtectedError
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.core.paginator import Paginator


from .models import Tipo, Grupo, Categoria, Conta, Pessoa, Movimento
from financeiro.forms import (
    TipoModelForm,
    GrupoModelForm,
    CategoriaModelForm, 
    ContaModelForm,
    PessoaModelForm, 
    MovimentoModelForm, 
    PagamentoModelForm,
    TransferenciaForm,
)
from .utils import (
    atualiza_saldo, 
    calcula_balanco, 
    calcula_pendentes, 
    calcula_vencidos_não_pagos,
    baixa_cartoes,
)
from .utils_charts import (
    despesas_variaveis_ano, 
    despesas_variaveis_mes, 
    despesas_categoria_ano,
    despesas_pessoas_categoria_ano,
)

@login_required
def financeiro(request):
    today = date.today()  
    ano = request.GET.get('ano')
    mes = request.GET.get('mes')
    if not ano:
        ano = today.year
    if not mes:
        mes = today.month

    categorias = Categoria.objects.filter(usuario=request.user).order_by('nome')
    categoria_id = request.GET.get('categoria_id')
    if not categoria_id:
        cat = categorias[0]
        categoria_id = cat.id
    categoria = Categoria.objects.get(id=categoria_id)
    contas, saldo_total, contas_outras= atualiza_saldo(request.user)
    receitas, despesas, balanco = calcula_balanco(request.user, ano, mes)
    despesas_fluxo, receitas_fluxo, saldo_pendentes = calcula_pendentes(saldo_total, request.user)
    vencidos = calcula_vencidos_não_pagos(request.user)
     # graficos despesas mes
    labels, data = despesas_variaveis_mes(ano, mes, request.user)
    labels_mes = json.dumps(labels)
    data_mes = json.dumps(data)
    # graficos variaveis ano
    labels, data = despesas_variaveis_ano(ano, mes, request.user)
    labels_ano = json.dumps(labels)
    data_ano = json.dumps(data)
    # graficos categorias no ano
    labels, data = despesas_categoria_ano(ano, mes, categoria_id, request.user)
    labels_categoria = json.dumps(labels)
    data_categoria = json.dumps(data)
    # graficos pessoas por categorias no mes
    labels, data = despesas_pessoas_categoria_ano(ano, mes, categoria_id, request.user)
    labels_pessoa = json.dumps(labels)
    data_pessoa = json.dumps(data) 
    # data da consulta
    ano = int(ano)
    mes = int(mes)
    data_consulta = date(ano, mes, 1)
   
    context = {
        'contas': contas,
        'contas_outras': contas_outras,
        'saldo_total': saldo_total,
        'despesas': despesas,
        'receitas': receitas,
        'balanco': balanco,
        'despesas_vencer': despesas_fluxo,
        'receitas_vencer': receitas_fluxo,
        'saldo_pendentes': saldo_pendentes,
        'vencidos': vencidos,
        'labels_ano': labels_ano,
        'data_ano': data_ano,
        'labels_mes': labels_mes,
        'data_mes': data_mes,
        'data_consulta': data_consulta,
        'categorias': categorias,
        'labels_categoria': labels_categoria,
        'data_categoria': data_categoria,
        'categoria': categoria,
        'labels_pessoa': labels_pessoa,
        'data_pessoa': data_pessoa,
    }
    return render(request, 'financeiro/financeiro.html', context)

##### Tipo de Categoria #####
class TipoList(LoginRequiredMixin, ListView):
    model = Tipo
    context_object_name = 'tipos'
    template_name = 'financeiro/tipo/list.html'
    paginate_by = 50

    def get_queryset(self):
        tipos = Tipo.objects.filter(usuario=self.request.user).order_by('ordem', 'nome')
        search = self.request.GET.get('search')
        if search:
            tipos = tipos.filter(nome__icontains=search)
        return tipos

class TipoCreate(LoginRequiredMixin, CreateView):
    model = Tipo
    form_class = TipoModelForm
    template_name = 'financeiro/tipo/form.html'
    success_url = reverse_lazy('financeiro:tipos')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'O Tipo foi criado com sucesso')
        return super(TipoCreate, self).form_valid(form)    

class TipoUpdate(LoginRequiredMixin, UpdateView):
    model = Tipo
    form_class = TipoModelForm
    template_name = 'financeiro/tipo/form.html'
    success_url = reverse_lazy('financeiro:tipos')

    def form_valid(self, form):
        messages.success(self.request, 'O Tipo foi alterado com sucesso')
        return super(TipoUpdate, self).form_valid(form)   

    def get_queryset(self):
        base_qs = super(TipoUpdate, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)

class TipoDelete(LoginRequiredMixin, DeleteView):
    model = Tipo
    template_name = 'financeiro/tipo/confirm_delete.html'
    success_url = reverse_lazy('financeiro:tipos')

    def form_valid(self, form):
        messages.success(self.request, 'O Tipo foi excluido com sucesso')
        return super(TipoDelete, self).form_valid(form)   
    
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Não é possível excluir este Tipo porque ele é referenciado por meio de chave protegida')
            return redirect('financeiro:tipos')

    def get_queryset(self):
        base_qs = super(TipoDelete, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)


##### Grupo de Categoria #####
class GrupoList(LoginRequiredMixin, ListView):
    model = Grupo
    context_object_name = 'grupos'
    template_name = 'financeiro/grupo/list.html'
    paginate_by = 50

    def get_queryset(self):
        grupos = Grupo.objects.filter(usuario=self.request.user).order_by('tipo', 'grupo', 'nome')
        search = self.request.GET.get('search')
        if search:
            grupos = grupos.filter(nome__icontains=search)
        return grupos

class GrupoCreate(LoginRequiredMixin, CreateView):
    model = Grupo
    form_class = GrupoModelForm
    template_name = 'financeiro/grupo/form.html'
    success_url = reverse_lazy('financeiro:grupos')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'O grupo foi criado com sucesso')
        return super(GrupoCreate, self).form_valid(form)    

class GrupoUpdate(LoginRequiredMixin, UpdateView):
    model = Grupo
    form_class = GrupoModelForm
    template_name = 'financeiro/grupo/form.html'
    success_url = reverse_lazy('financeiro:grupos')

    def form_valid(self, form):
        messages.success(self.request, 'O Grupo foi alterado com sucesso')
        return super(GrupoUpdate, self).form_valid(form)   

    def get_queryset(self):
        base_qs = super(GrupoUpdate, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)

class GrupoDelete(LoginRequiredMixin, DeleteView):
    model = Grupo
    template_name = 'financeiro/grupo/confirm_delete.html'
    success_url = reverse_lazy('financeiro:grupos')

    def form_valid(self, form):
        messages.success(self.request, 'O Grupo foi excluido com sucesso')
        return super(GrupoDelete, self).form_valid(form)   
    
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Não é possível excluir este Grupo porque ele é referenciado por meio de chave protegida: Movimento.grupo')
            return redirect('financeiro:grupos')

    def get_queryset(self):
        base_qs = super(GrupoDelete, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)


##### Categoria #####
class CategoriaList(LoginRequiredMixin, ListView):
    model = Categoria
    context_object_name = 'categorias'
    template_name = 'financeiro/categoria/list.html'
    paginate_by = 50

    def get_queryset(self):
        categorias = Categoria.objects.filter(usuario=self.request.user).order_by('nome')
        search = self.request.GET.get('search')
        if search:
            categorias = categorias.filter(nome__icontains=search)
        return categorias


# CBV - CreateView - Criação
class CategoriaCreate(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaModelForm
    template_name = 'financeiro/categoria/form.html'
    success_url = reverse_lazy('financeiro:categorias')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'A Categoria foi criada com sucesso')
        return super(CategoriaCreate, self).form_valid(form)

# CBV - UpdateView - Alteração
class CategoriaUpdate(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaModelForm
    template_name = 'financeiro/categoria/form.html'
    success_url = reverse_lazy('financeiro:categorias')

    def form_valid(self, form):
        messages.success(self.request, 'A Categoria foi alterada com sucesso')
        return super(CategoriaUpdate, self).form_valid(form)   

    def get_queryset(self):
        base_qs = super(CategoriaUpdate, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)

# CBV - DeleteView - Deleção
class CategoriaDelete(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'financeiro/categoria/confirm_delete.html'
    success_url = reverse_lazy('financeiro:categorias')

    def form_valid(self, form):
        messages.success(self.request, 'A Categoria foi excluida com sucesso')
        return super(CategoriaDelete, self).form_valid(form)   
    
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Não é possível excluir esta Categoria porque ela é referenciada por meio de chave protegida: Movimento.categoria')
            return redirect('financeiro:categorias')

    def get_queryset(self):
        base_qs = super(CategoriaDelete, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)




##### Contas #####
# CBV - ListView - Listagem
class ContasList(LoginRequiredMixin, ListView):
    model = Conta
    context_object_name = 'contas'
    template_name = 'financeiro/conta/list.html'
    paginate_by = 50

    def get_queryset(self):
        contas = Conta.objects.filter(usuario=self.request.user).order_by('nome')
        search = self.request.GET.get('search')
        if search:
            contas = contas.filter(nome__icontains=search)
        return contas
    
# CBV - CreateView - Criação
class ContaCreate(LoginRequiredMixin, CreateView):
    model = Conta
    form_class = ContaModelForm
    template_name = 'financeiro/conta/form.html'
    success_url = reverse_lazy('financeiro:contas')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'A Conta foi criada com sucesso')
        return super(ContaCreate, self).form_valid(form)
        
# CBV - UpdateView - Alteração
class ContaUpdate(LoginRequiredMixin, UpdateView):
    model = Conta
    form_class = ContaModelForm
    template_name = 'financeiro/conta/form.html'
    success_url = reverse_lazy('financeiro:contas')

    def form_valid(self, form):
        messages.success(self.request, 'A Conta foi alterada com sucesso')
        return super(ContaUpdate, self).form_valid(form)   

    def get_queryset(self):
        base_qs = super(ContaUpdate, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)

# CBV - DeleteView - Deleção
class ContaDelete(LoginRequiredMixin, DeleteView):
    model = Conta
    template_name = 'financeiro/conta/confirm_delete.html'
    success_url = reverse_lazy('financeiro:contas')

    def form_valid(self, form):
        messages.success(self.request, 'A Conta foi excluida com sucesso')
        return super(ContaDelete, self).form_valid(form)   
    
    def get_queryset(self):
        base_qs = super(ContaDelete, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)
    
##### Pessoas #####
# CBV - ListView - Listagem
class PessoasList(LoginRequiredMixin, ListView):
    model = Pessoa
    context_object_name = 'pessoas'
    template_name = 'financeiro/pessoa/list.html'
    paginate_by = 50

    def get_queryset(self):
        pessoas = Pessoa.objects.filter(usuario=self.request.user).order_by('nome')
        search = self.request.GET.get('search')
        if search:
            pessoas = pessoas.filter(nome__icontains=search)
        return pessoas
    
# CBV - CreateView - Criação
class PessoaCreate(LoginRequiredMixin, CreateView):
    model = Pessoa
    form_class = PessoaModelForm
    template_name = 'financeiro/pessoa/form.html'
    success_url = reverse_lazy('financeiro:pessoas')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'A Pessoa foi criada com sucesso')
        return super(PessoaCreate, self).form_valid(form)


# CBV - UpdateView - Alteração
class PessoaUpdate(LoginRequiredMixin, UpdateView):
    model = Pessoa
    form_class = PessoaModelForm
    template_name = 'financeiro/pessoa/form.html'
    success_url = reverse_lazy('financeiro:pessoas')

    def form_valid(self, form):
        messages.success(self.request, 'A Pessoa foi alterada com sucesso')
        return super(PessoaUpdate, self).form_valid(form)   

    def get_queryset(self):
        base_qs = super(PessoaUpdate, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)

# CBV - DeleteView - Deleção
class PessoaDelete(LoginRequiredMixin, DeleteView):
    model = Pessoa
    template_name = 'financeiro/pessoa/confirm_delete.html'
    success_url = reverse_lazy('financeiro:pessoas')

    def form_valid(self, form):
        messages.success(self.request, 'A Pessoa foi excluida com sucesso')
        return super(PessoaDelete, self).form_valid(form)   
    
    def get_queryset(self):
        base_qs = super(PessoaDelete, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)
 
##### Movimento #####
def MovimentoList(request):
    template_name = 'financeiro/movimento/list.html'
    contas = Conta.objects.filter(usuario=request.user).order_by('nome')

    data_inicio = request.GET.get('data_inicio')
    data_final = request.GET.get('data_final')
    conta = request.GET.get('conta')

    if not data_inicio or not data_final:
        today = date.today()
        data_inicio = date(today.year, today.month, 1)
        data_final = data_inicio.replace(day=monthrange(data_inicio.year, data_inicio.month)[1])

    movimento = Movimento.objects.filter(
        usuario=request.user, data_vencimento__range=[data_inicio, data_final]).order_by('-data_vencimento', '-created_at')
    
    if conta:
        movimento = movimento.filter(conta__id=conta)
     
    paginator = Paginator(movimento, 50) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'contas': contas,
        'page_obj': page_obj,
    }
    return render(request, template_name, context)
    

# CBV - CreateView - Criação
class MovimentoCreate(LoginRequiredMixin, CreateView):
    model = Movimento
    form_class = MovimentoModelForm
    template_name = 'financeiro/movimento/form.html'
    success_url = reverse_lazy('financeiro:movimentos')

    def get_initial(self):
        return {'usuario':self.request.user}
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'O Movimento foi criado com sucesso')
        return super(MovimentoCreate, self).form_valid(form)

# CBV - UpdateView - Alteração
class MovimentoUpdate(LoginRequiredMixin, UpdateView):
    model = Movimento
    form_class = MovimentoModelForm
    template_name = 'financeiro/movimento/form.html'
    success_url = reverse_lazy('financeiro:movimentos')

    def get_initial(self):
        return {'usuario':self.request.user}
    
    def form_valid(self, form):
        messages.success(self.request, 'O Movimento foi alterado com sucesso')
        return super(MovimentoUpdate, self).form_valid(form)   

    def get_queryset(self):
        base_qs = super(MovimentoUpdate, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)
    
# CBV - DeleteView - Deleção
class MovimentoDelete(LoginRequiredMixin, DeleteView):
    model = Movimento
    template_name = 'financeiro/movimento/confirm_delete.html'
    success_url = reverse_lazy('financeiro:movimentos')

    def form_valid(self, form):
        messages.success(self.request, 'A movimentação foi excluida com sucesso')
        return super(MovimentoDelete, self).form_valid(form)   
    
    def get_queryset(self):
        base_qs = super(MovimentoDelete, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)
 
# CBV - UpdateView - Pagamento
class PagamentoUpdate(LoginRequiredMixin, UpdateView):
    model = Movimento
    form_class = PagamentoModelForm
    template_name = 'financeiro/movimento/form-pagamento.html'
    success_url = reverse_lazy('financeiro:financeiro')

    def form_valid(self, form):
        messages.success(self.request, 'O Pagamento foi efetuado com sucesso')
        return super(PagamentoUpdate, self).form_valid(form)   

    def get_queryset(self):
        base_qs = super(PagamentoUpdate, self).get_queryset()
        return base_qs.filter(usuario=self.request.user)

# FBV - Transferencia
@login_required
def Transferencia(request):
    template_name = 'financeiro/movimento/form-transferencia.html'
    form = TransferenciaForm(request.user, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            data = request.POST.get('data_transferencia')
            conta_origem = request.POST.get('conta_origem')
            conta_destino = request.POST.get('conta_destino')
            categoria = request.POST.get('categoria')
            pessoa = request.POST.get('pessoa')
            valor = request.POST.get('valor')
        
            movimento = Movimento(
                data_vencimento = data,
                data_pagamento = data,
                conta_id=conta_origem,
                categoria_id=categoria,
                pessoa_id=pessoa,
                valor=valor,
                tipo='D',
                usuario=request.user,
            )
            movimento.save()
            movimento = Movimento(
                data_vencimento = data,
                data_pagamento = data,
                conta_id=conta_destino,
                categoria_id=categoria,
                pessoa_id=pessoa,
                valor=valor,
                tipo='R',
                usuario=request.user,
            )
            movimento.save()
            return redirect('financeiro:movimentos')

    context = {'form': form}
    return render(request, template_name, context)

# FBV - ListView - Listagem de cartões
@login_required
def CartoesList(request):
    cartoes = []
    conta_id = 0
    data_vencimento = None
    data_pagamento = None
    total_cartao = 0

    template_name = 'financeiro/movimento/list_cartoes.html'

    contas = Conta.objects.filter(usuario=request.user, tipo='CT').order_by('nome')
    contas_debito = Conta.objects.filter(usuario=request.user, tipo='CC').order_by('nome')
    categorias = Categoria.objects.filter(usuario=request.user, tipo='TR')
    pessoas = Pessoa.objects.filter(usuario=request.user).order_by('nome')
    
    if request.method == 'GET':
        conta_id = request.GET.get('conta')
        data_vencimento = request.GET.get('data-vencimento')

    if conta_id and data_vencimento:
        cartoes = Movimento.objects.filter(
            usuario=request.user, conta__id=conta_id, data_vencimento=data_vencimento, tipo='D')
        total_cartao = cartoes.filter(data_pagamento__isnull=True).aggregate(Sum('valor'))['valor__sum']
        if not total_cartao:
            total_cartao = 0

    if request.method == 'POST':
        data_pagamento = request.POST.get('data-pagamento')
        conta_debito = request.POST.get('conta-debito')
        categoria = request.POST.get('categoria')
        pessoa = request.POST.get('pessoa')
        conta_id = request.GET.get('conta')
        data_vencimento = request.GET.get('data-vencimento')

    if data_pagamento:
        baixa_cartoes(
            request.user, 
            data_pagamento, 
            conta_debito, 
            categoria, 
            pessoa , 
            conta_id , 
            data_vencimento
        )
       
    cartoes = Movimento.objects.filter(
        usuario=request.user, conta__id=conta_id, data_vencimento=data_vencimento, tipo='D')
    total_cartao = cartoes.filter(data_pagamento__isnull=True).aggregate(Sum('valor'))['valor__sum']
    if not total_cartao:
        total_cartao = 0

    context = {
        'contas': contas,
        'cartoes': cartoes,
        'total_cartao': total_cartao,
        'contas_debito': contas_debito,
        'categorias': categorias,
        'pessoas': pessoas,
    }   

    return render(request, template_name, context)

def extrato_list(request):
    template_name = 'financeiro/movimento/extrato_list.html'
    contas = Conta.objects.filter(usuario=request.user).order_by('nome')

    data_inicio = request.GET.get('data_inicio')
    data_final = request.GET.get('data_final')
    conta = request.GET.get('conta')

    if not data_inicio or not data_final:
        today = date.today()
        data_inicio = date(today.year, today.month, 1)
        data_final = data_inicio.replace(day=monthrange(data_inicio.year, data_inicio.month)[1])

    movimento = Movimento.objects.filter(
        usuario=request.user, data_vencimento__range=[data_inicio, data_final]).order_by('data_vencimento')
    
    if conta:
        movimento = movimento.filter(conta__id=conta)
        
    despesas = movimento.filter(tipo='D').exclude(categoria__tipo='TR').aggregate(Sum('valor'))['valor__sum']
    receitas = movimento.filter(tipo='R').exclude(categoria__tipo='TR').aggregate(Sum('valor'))['valor__sum']

    paginator = Paginator(movimento, 50) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'contas': contas,
        'page_obj': page_obj,
        'despesas': despesas,
        'receitas': receitas,
    }
    return render(request, template_name, context)
