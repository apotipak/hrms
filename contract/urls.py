from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.ContractList, name='contract-list'),
    path('contract/create', views.contract_create, name='contract_create'),
    path('contract/<int:pk>/update', views.ContractUpdate, name='contract-update'),
    url(r'^ajax/save_contract/$', views.SaveContract, name='save-contract'),
    url(r'^ajax/get_wagerate_list/$', views.get_wagerate_list, name='get_wagerate_list'),
    url(r'^ajax/get_wagerate_list_modal/$', views.get_wagerate_list_modal, name='get_wagerate_list_modal'),
    url(r'^ajax/update_customer_service/$',views.update_customer_service, name='update_customer_service'),
    url(r'^ajax/save_customer_service_item/$',views.save_customer_service_item, name='save_customer_service_item'),    
]
