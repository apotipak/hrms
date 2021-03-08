from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.ContractListReport, name='contract_list_report'),    
    url(r'^ajax/report_search_contract/$', views.AJAXReportSearchContract, name='report_search_contract'),
]
