from django.urls import path
from .views import (
    financeiro,
    TipoList,
    TipoCreate,
    TipoUpdate,
    TipoDelete,
    GrupoList,
    GrupoCreate,
    GrupoUpdate, 
    GrupoDelete,
    CategoriaList, 
    CategoriaCreate,
    CategoriaUpdate, 
    CategoriaDelete,
    ContasList,
    ContaCreate,
    ContaUpdate, 
    ContaDelete,
    PessoasList,
    PessoaCreate,
    PessoaUpdate, 
    PessoaDelete,
    MovimentoList,
    MovimentoCreate,
    MovimentoUpdate,
    MovimentoDelete,
    PagamentoUpdate,
    Transferencia,
    CartoesList,
    extrato_list,
    extrato_mensal,
    definir_planejamento,
    update_valor_categoria,
    ver_planejamento,
)

app_name = 'financeiro'

urlpatterns = [
    path('', financeiro, name='financeiro'),
    # Tipo
    path('tipos/', TipoList.as_view(), name='tipos'),
    path('tipo/create/', TipoCreate.as_view(), name='tipo-create'),
    path('tipo/update/<int:pk>', TipoUpdate.as_view(), name='tipo-update'),
    path('tipo/delete/<int:pk>', TipoDelete.as_view(), name='tipo-delete'),
    # Grupo
    path('grupos/', GrupoList.as_view(), name='grupos'),
    path('grupo/create/', GrupoCreate.as_view(), name='grupo-create'),
    path('grupo/update/<int:pk>', GrupoUpdate.as_view(), name='grupo-update'),
    path('grupo/delete/<int:pk>', GrupoDelete.as_view(), name='grupo-delete'),
    # Categoria
    path('categorias/', CategoriaList.as_view(), name='categorias'),
    path('categoria/create/', CategoriaCreate.as_view(), name='categoria-create'),
    path('categoria/update/<int:pk>', CategoriaUpdate.as_view(), name='categoria-update'),
    path('categoria/delete/<int:pk>', CategoriaDelete.as_view(), name='categoria-delete'),
    # Conta
    path('contas/', ContasList.as_view(), name='contas'),
    path('conta/create/', ContaCreate.as_view(), name='conta-create'),
    path('conta/update/<int:pk>', ContaUpdate.as_view(), name='conta-update'),
    path('conta/delete/<int:pk>', ContaDelete.as_view(), name='conta-delete'),
    # Pessoa
    path('pessoas/', PessoasList.as_view(), name='pessoas'),
    path('pessoa/create/', PessoaCreate.as_view(), name='pessoa-create'),
    path('pessoa/update/<int:pk>', PessoaUpdate.as_view(), name='pessoa-update'),
    path('pessoa/delete/<int:pk>', PessoaDelete.as_view(), name='pessoa-delete'),
    # Movimento
    path('movimentos/', MovimentoList, name='movimentos'),
    path('movimento/create/', MovimentoCreate.as_view(), name='movimento-create'),
    path('movimento/update/<int:pk>', MovimentoUpdate.as_view(), name='movimento-update'),
    path('movimento/delete/<int:pk>', MovimentoDelete.as_view(), name='movimento-delete'),
    # Pagamento
    path('pagamento/update/<int:pk>', PagamentoUpdate.as_view(), name='pagamento-update'),
    # tranferencia
    path('transferencia/', Transferencia, name='transferencia'),
    # cartão de crédito
    path('cartoes/', CartoesList, name='cartoes'),
    # extratos
    path('extrato_list/', extrato_list, name='extrato-list'), 
    path('extrato_mensal/', extrato_mensal, name='extrato-mensal'), 
     # ḉanejamento
    path('definir_planejamento/', definir_planejamento, name='definir_planejamento'), 
    path('update_valor_categoria/<int:id>', update_valor_categoria, name="update_valor_categoria"),
    path('ver_planejamento/', ver_planejamento, name='ver_planejamento')
]
