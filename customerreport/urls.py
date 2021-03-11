from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    
    path('export-customer-main-address/', views.ExportCustomerAddressMainReport, name='export-customer-main-address'),
    url(r'^ajax-search-customer-main-address/$', views.AjaxSearchCustomerMainAddress, name='ajax-search-customer-main-address'),
    url(r'^ajax-export-customer-main-address/(?P<customer_zone>\w+)/$', views.export_customer_main_addres, name='ajax-export-customer-main-address'),
]
