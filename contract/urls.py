from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.ContractList, name='contract-list'),
    path('contract/create', views.contract_create, name='contract_create'),
    path('contract/<int:pk>/update', views.ContractUpdate, name='contract-update'),
    url(r'^ajax/update_contract/$', views.UpdateContract, name='update-contract'),
    url(r'^ajax/create_contract/$', views.CreateContract, name='create-contract'),
    url(r'^ajax/get_wagerate_list/$', views.get_wagerate_list, name='get_wagerate_list'),
    url(r'^ajax/get_wagerate_list_modal/$', views.get_wagerate_list_modal, name='get_wagerate_list_modal'),
    url(r'^ajax/update_customer_service/$',views.update_customer_service, name='update_customer_service'),
    url(r'^ajax/save_customer_service_item/$',views.save_customer_service_item, name='save_customer_service_item'),

    url(r'^ajax/get_cus_main/$', views.get_cus_main, name='get_cus_main'),
    url(r'^ajax/get_customer/$', views.get_customer, name='get_customer'),
    url(r'^ajax/get_cus_contract/$', views.get_cus_contract, name='get_cus_contract'),
]
