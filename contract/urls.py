from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.ContractList, name='contract-list'),
    
    # path('contract/create', views.contract_create, name='contract_create'),
    path('contract/manage', views.contract_create, name='contract_create'),

    # path('contract/<int:pk>/update', views.ContractUpdate, name='contract-update'),
    # url(r'^ajax/update_contract/$', views.UpdateContract, name='update-contract'),
    url(r'^ajax/create_contract/$', views.CreateContract, name='create-contract'),
    
    url(r'^ajax/get_wagerate_list/$', views.get_wagerate_list, name='get_wagerate_list'),
    
    url(r'^ajax/get_contract_list/$', views.get_contract_list, name='get_contract_list'),
    url(r'^ajax/get_contract_list_modal/$', views.get_contract_list_modal, name='get_contract_list_modal'),

    url(r'^ajax/get_wagerate_list_modal/$', views.get_wagerate_list_modal, name='get_wagerate_list_modal'),    

    url(r'^ajax/update_customer_service/$', views.update_customer_service, name='update_customer_service'),
    url(r'^ajax/save_new_service/$', views.save_new_service, name='save_new_service'),
    url(r'^ajax/add_new_service/$', views.add_new_service, name='add_new_service'),
    url(r'^ajax/save_customer_service_item/$', views.save_customer_service_item, name='save_customer_service_item'),
    url(r'^ajax/get_cus_main/$', views.get_cus_main, name='get_cus_main'),
    url(r'^ajax/get_customer/$', views.get_customer, name='get_customer'),
    url(r'^ajax/get_cus_contract/$', views.get_cus_contract, name='get_cus_contract'),
    url(r'^ajax/get_rank_shift_list/$', views.get_rank_shift_list, name='get_rank_shift_list'),
    url(r'^ajax/reload_service_list/$', views.reload_service_list, name='reload_service_list'),
    url(r'^ajax/reload_contract_list/$', views.reload_contract_list, name='reload_contract_list'),
    url(r'^ajax/delete_customer_service/$', views.delete_customer_service, name='delete_customer_service'),
    url(r'^ajax/delete_customer_contract/$', views.delete_customer_contract, name='delete_customer_contract'),
    
    # url(r'^generate-contract/(?P<cnt_id>\d+)/$', views.generate_contract, name='generate_contract'),
    # url(r'^generate-contract/(?P<cnt_id>\d+)/(?P<language_option>\w+)/$', views.generate_contract, name='generate-contract'),
    url(r'^generate-contract/(?P<cnt_id>\d+)/(?P<language_option>\w+)/(?P<is_new_report>\w+)/(?P<is_amendment>\w+)/(?P<is_customer_address>\w+)/$', views.generate_contract, name='generate-contract'),
    url(r'^download-contract/(?P<cnt_id>\d+)/(?P<language_option>\w+)/(?P<is_new_report>\w+)/(?P<is_amendment>\w+)/(?P<is_customer_address>\w+)/$', views.download_contract, name='download-contract'),
    #url(r'^download-contract/(?P<file_name>[-\w_\\-\\.]+)$', views.download_contract, name='download-contract'),
    url(r'^print-contract/(?P<file_name>[-\w_\\-\\.]+)$', views.print_contract, name='print-contract'),
    url(r'^ajax/ajax_undelete_contract/$', views.ajax_undelete_contract, name='ajax_undelete_contract'),
]
