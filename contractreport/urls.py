from django.conf.urls import url
from django.urls import path
from django.urls import re_path
from . import views


urlpatterns = [
    path('', views.ContractListReport, name='contract_list_report'),    
    url(r'^ajax/report_search_contract/$', views.AJAXReportSearchContract, name='report_search_contract'),    
    url(r'^generate-contract-list/(?P<contract_number_from>\w+)/(?P<contract_number_to>\w+)/(?P<contract_status>\w+)/(?P<contract_zone>\w+)/$', views.generate_contract_list, name='generate-contract-list'),
]


urlpatterns += [
    url(r'^generate-contract-list/(?P<contract_number_from>\w+)/(?P<contract_number_to>\w+)/(?P<contract_status>\w+)/(?P<contract_zone>\w+)/$', views.generate_contract_list, name='generate-contract-list'),
    url(r'^export-contract-list/(?P<contract_number_from>\w+)/(?P<contract_number_to>\w+)/(?P<contract_status>\w+)/(?P<contract_zone>\w+)/$', views.export_contract_list_report, name='export_contract_list_report'),
    # url(r'^export/xls/$', views.export_contract_list_report, name='export_contract_list_report'),
]