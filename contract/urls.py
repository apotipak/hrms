from django.urls import path
from . import views


urlpatterns = [
    #path('', views.ContractList, name='contract-list'),
    path('', views.ContractCreate, name='contract-list'),
    path('contract/create', views.ContractCreate, name='contract_create'),
    path('search_contract_number', views.SearchContractNumber, name='search_contract_number'),
]
