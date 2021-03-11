from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    
    # path('export-customer-address-main/', views.ExportCustomerAddressMainReport, name='export-customer-address-main-report'),
    path('', views.ExportCustomerAddressMainReport, name='export-customer-address-main-report'),    
]
