from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    
    # GPM 403 Daily Guary Performance Report by Contract
    # path('', views.GPM403DailyGuardPerformanceReport, name='gpm403-daily-guard-performance-by-contract'),
    path('gpm-403-daily-guard-performance-by-contract/', views.GPM403DailyGuardPerformanceReport, name='gpm-403-daily-guard-performance-by-contract'),
    url(r'^gpm-403-daily-guard-performance-by-contract/(?P<contract_number_from>\d+)/(?P<contract_number_to>\d+)/(?P<start_date>\d{2}/\d{2}/\d{4})/(?P<end_date>\d{2}/\d{2}/\d{4})/$', views.GenerateGPM403DailyGuardPerformanceReport, name='gpm-403-daily-guard-performance-by-contract'),
    path('ajax-gpm-403-daily-guard-performance-by-contract/', views.AjaxGPM403DailyGuardPerformanceReport, name='ajax-gpm-403-daily-guard-performance-by-contract'),
    url(r'^export-gpm-403-daily-guard-performance-by-contract-to-excel/(?P<contract_number_from>\d+)/(?P<contract_number_to>\d+)/(?P<start_date>\d{2}/\d{2}/\d{4})/(?P<end_date>\d{2}/\d{2}/\d{4})/$', views.export_gpm_403_daily_guard_performance_by_contract_to_excel, name='export-gpm-403-daily-guard-performance-by-contract-to-excel'),

    # GPM Work on Day Off
    path('gpm-work-on-day-off-day-off/', views.GPMWorkOnDayOffReport, name='gpm-work-on-day-off-day-off'),
    url(r'^ajax-gpm-work-on-day-off/(?P<start_date>\d{2}/\d{2}/\d{4})/(?P<end_date>\d{2}/\d{2}/\d{4})/$', views.AjaxGPMWorkOnDayOffReport, name='ajax-gpm-work-on-day-off-report'),
    url(r'^export-gpm-work-on-day-off-to-excel/(?P<start_date>\d{2}/\d{2}/\d{4})/(?P<end_date>\d{2}/\d{2}/\d{4})/$', views.export_gpm_work_on_day_off_to_excel, name='export-gpm-work-on-day-off-to-excel'),

    # GPM 422 No. of Guard Operation by Empl by Zone    
    path('gpm-422-no-of-guard-operation-by-empl-by-zone/', views.GPM422NoOfGuardOperationByEmplByZoneReport, name='gpm-422-no-of-guard-operation-by-empl-by-zone-report'),
    url(r'^ajax-gpm-422-no-of-guard-operation-by-empl-by-zone/(?P<start_date>\d{2}/\d{2}/\d{4})/(?P<end_date>\d{2}/\d{2}/\d{4})/(?P<dept_zone>\d+)/$', views.AjaxGPM422NoOfGuardOperationByEmplByZoneReport, name='ajax-gpm-422-no-of-guard-operation-by-empl-by-zone'),
    url(r'^export-gpm-422-no-of-guard-operation-by-empl-by-zone-to-excel/(?P<start_date>\d{2}/\d{2}/\d{4})/(?P<end_date>\d{2}/\d{2}/\d{4})/(?P<dept_zone>\d+)/$', views.export_gpm_422_no_of_guard_operation_by_empl_by_zone_to_excel, name='export-gpm-422-no-of-guard-operation-by-empl-by-zone-to-excel'),

    # Post Manpower
    path('post-manpower/', views.PostManpowerReport, name='post-manpower-report'),  
    url(r'^ajax-post-manpower/$', views.AjaxPostManpowerReport, name='ajax-post-manpower-report'),
    url(r'^export-post-manpower-to-excel/(?P<contract_number_from>\d+)/(?P<contract_number_to>\d+)/(?P<contract_start_date>\d{2}/\d{2}/\d{4})/(?P<contract_end_date>\d{2}/\d{2}/\d{4})/(?P<contract_zone_id>\w+)/$', views.export_post_manpower_to_excel, name='export-post-manpower-to-excel'),

    # PSN Slip D1 Report
    path('psn-slip-d1/', views.PSNSlipD1Report, name='psn-slip-d1-report'),
    url(r'^ajax-validate-psn-slip-d1-period/', views.AjaxValidatePSNSlipD1Period, name='ajax-validate-psn-slip-d1-period'),
    url(r'^generate-psn-slip-d1/(?P<emp_id>\d+)/(?P<period>\w+)/$', views.GeneratePSNSlipD1, name='generate-psn-slip-d1'),

    # Income / Dedcut D1 Report
    path('income-deduct-d1/', views.IncomeDeductD1Report, name='income-deduct-d1-report'),
    path('ajax-search-income-deduct-d1/', views.AjaxSearchIncomeDeductD1, name='ajax-search-income-deduct-d1'),

    # Terminate Employee List
    path('terminate-employee-list/', views.TerminateEmployeeListReport, name='terminate-employee-list'),
    path('ajax-terminate-employee-list/', views.AjaxTerminateEmployeeListReport, name='ajax-terminate-employee-list'),

]
