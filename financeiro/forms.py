from datetime import timezone
from django.conf import Settings
from django.contrib.auth.models import User
from django import forms
from financeiro.models import Grupo, Categoria, Conta, Pessoa, Movimento

class GrupoModelForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['tipo', 'nome' ]
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            self.add_error('nome', 'O nome deve ter trẽs ou mais caracteres.')
        return nome
    

class CategoriaModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoriaModelForm, self).__init__(*args, **kwargs)
        usuario = kwargs['initial']['usuario']
        self.fields['grupo'].queryset = Grupo.objects.filter(usuario=usuario)
    class Meta:
        model = Categoria
        fields = ['tipo', 'grupo', 'nome']
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')

        if len(nome) < 3:
            self.add_error('nome', 'O nome deve ter trẽs ou mais caracteres.')
        return nome
    

class ContaModelForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'tipo', 'saldo_inicial', 'logo']
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')

        if len(nome) < 3:
            self.add_error('nome', 'O nome deve ter trẽs ou mais caracteres.')
        return nome


class PessoaModelForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome']
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')

        if len(nome) < 3:
            self.add_error('nome', 'O nome deve ter trẽs ou mais caracteres.')
        return nome
    

class MovimentoModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MovimentoModelForm, self).__init__(*args, **kwargs)
        usuario = kwargs['initial']['usuario']
        self.fields['conta'].queryset = Conta.objects.filter(usuario=usuario)
        self.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)
        self.fields['pessoa'].queryset = Pessoa.objects.filter(usuario=usuario)
        
    data_vencimento = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),)
    data_pagamento = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),required=False)
    class Meta:
        model = Movimento
        fields = ['data_vencimento', 'data_pagamento', 'conta', 'categoria', 'pessoa', 'descricao', 'valor', 'tipo']
     
class PagamentoModelForm(forms.ModelForm):
    data_pagamento = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),required=False)
    class Meta:
        model = Movimento
        fields = ['data_pagamento']

class TransferenciaForm(forms.Form):
    data_transferencia = forms.DateField(
        label='Data da Transferencia',
        widget=forms.TextInput(attrs={'type': 'date'}),
        required=True
    )
    
    conta_destino = forms.ChoiceField(
        label='Conta de Destino',
        required=True,
    )
    conta_origem = forms.ChoiceField(
        label='Conta de Origem',
        required=True,
    )
    categoria = forms.ChoiceField(
        label='Categoria',
        required=True,
    )
    pessoa = forms.ChoiceField(
        label='Pessoa',
        required=True,
    )
    valor = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Valor da Transferencia',
        required=True,
    )

    def __init__(self, user=None, *args, **kwargs):
        super(TransferenciaForm, self).__init__(*args, **kwargs)
        CONTA_OPTIONS = [(conta.id, conta) for conta in Conta.objects.filter(usuario=user)]
        CATEGORIA_OPTIONS = [(categoria.id, categoria) for categoria in Categoria.objects.filter(usuario=user, tipo='TR')]
        PESSOA_OPTIONS = [(pessoa.id, pessoa) for pessoa in Pessoa.objects.filter(usuario=user)]
        self.fields['conta_origem'].choices = CONTA_OPTIONS
        self.fields['conta_destino'].choices = CONTA_OPTIONS
        self.fields['categoria'].choices = CATEGORIA_OPTIONS
        self.fields['pessoa'].choices = PESSOA_OPTIONS

