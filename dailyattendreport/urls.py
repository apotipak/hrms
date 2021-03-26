from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    
    # path('export-customer-main-address/', views.ExportCustomerMainAddressReport, name='export-customer-main-address'),
    # url(r'^ajax-search-customer-main-address/$', views.AjaxSearchCustomerMainAddress, name='ajax-search-customer-main-address'),
    # url(r'^ajax-export-customer-main-address/(?P<customer_zone>\w+)/$', views.export_customer_main_address, name='ajax-export-customer-main-address'),

    path('', views.GPM403DailyGuardPerformanceReport, name='gpm403-daily-guard-performance-by-contract'),
    path('gpm403-daily-guard-performance-by-contract/', views.GPM403DailyGuardPerformanceReport, name='gpm403-daily-guard-performance-by-contract'),
    path('ajax-gpm403-daily-guard-performance-by-contract/', views.AjaxGPM403DailyGuardPerformanceReport, name='ajax-gpm403-daily-guard-performance-by-contract'),

    path('gpm-work-on-day-off-day-off/', views.GPMWorkOnDayOffReport, name='gpm-work-on-day-off-day-off'),
    # path('ajax-gpm-work-on-day-off-day-off/', views.AjaxGPMWorkOnDayOffReport, name='ajax-gpm-work-on-day-off-day-off'),
]
