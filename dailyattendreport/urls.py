from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    
    # GPM 403 Daily Guary Performance Report by Contract
    path('', views.GPM403DailyGuardPerformanceReport, name='gpm403-daily-guard-performance-by-contract'),
    path('gpm403-daily-guard-performance-by-contract/', views.GPM403DailyGuardPerformanceReport, name='gpm403-daily-guard-performance-by-contract'),
    path('ajax-gpm403-daily-guard-performance-by-contract/', views.AjaxGPM403DailyGuardPerformanceReport, name='ajax-gpm403-daily-guard-performance-by-contract'),
    url(r'^export-gpm-403-to-excel/$', views.export_gpm_403_daily_guard_performance_by_contract_to_excel, name='export-gpm-403-daily-guard-performance-by-contract-to-excel'),
  	url(r'^gpm-403-daily-guard-performance-by-contract/(?P<contract_number_from>\d+)/(?P<contract_number_to>\d+)/(?P<start_date>\d{2}/\d{2}/\d{4})/(?P<end_date>\d{2}/\d{2}/\d{4})/$', views.GenerateGPM403DailyGuardPerformanceReport, name='gpm-403-daily-guard-performance-by-contract'),

    # GPM Work on Day Off
    path('gpm-work-on-day-off-day-off/', views.GPMWorkOnDayOffReport, name='gpm-work-on-day-off-day-off'),
    url(r'^ajax-gpm-work-on-day-off/(?P<start_date>\d{2}/\d{2}/\d{4})/$', views.AjaxGPMWorkOnDayOffReport, name='ajax-gpm-work-on-day-off-report'),

    # GPM 422 No. of Guard Operation by Empl by Zone    
    path('gpm-422-no-of-guard-operation-by-empl-by-zone/', views.GPM422NoOfGuardOperationByEmplByZoneReport, name='gpm-422-no-of-guard-operation-by-empl-by-zone-report'),    
    url(r'^ajax-gpm-422-no-of-guard-operation-by-empl-by-zone/(?P<work_date>\d{2}/\d{2}/\d{4})/(?P<dept_zone>\d+)/$', views.AjaxGPM422NoOfGuardOperationByEmplByZoneReport, name='ajax-gpm-422-no-of-guard-operation-by-empl-by-zone'),
]
