from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.ContractList, name='contract-list'),
    path('contract/<int:pk>/update', views.ContractUpdate, name='contract-update'),
    url(r'^ajax/save_contract/$', views.SaveContract, name='save-contract'),
    url(r'^ajax/get_wagerate_list/$', views.get_wagerate_list, name='get_wagerate_list'),
]
