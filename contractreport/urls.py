from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.ContractListReport, name='contract_list_report'),    
    url(r'^ajax/report_search_contract/$', views.AJAXReportSearchContract, name='report_search_contract'),
    url(r'^generate-contract-list/(?P<contract_number_from>\w+)/(?P<contract_number_to>\w+)/(?P<contract_status>\w+)/(?P<contract_zone>\w+)/$', views.generate_contract_list, name='generate-contract-list'),
]
