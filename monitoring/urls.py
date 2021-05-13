from django.urls import path, re_path, include
from . import views
from django.conf.urls import url


urlpatterns = [    
    path('', views.ScheduleMaintenance, name='daily-monitoring'),
    path('schedule-maintenance/', views.ScheduleMaintenance, name='schedule-maintenance'),
    url(r'^ajax/get_customer/$', views.ajax_get_customer, name='ajax_get_customer'),
    url(r'^ajax/get_customer_schdule_plan_list/$', views.ajax_get_customer_schedule_plan_list, name='ajax_get_customer_schedule_plan_list'),
    url(r'^ajax/get_customer_schdule_plan/$', views.ajax_get_customer_schedule_plan, name='ajax_get_customer_schedule_plan'),
    url(r'^ajax/save_customer_schdule_plan/$', views.ajax_save_customer_schedule_plan, name='ajax_save_customer_schedule_plan'),
    url(r'^ajax/get_employee_list/$', views.ajax_get_employee_list, name='ajax_get_employee_list'),
    url(r'^ajax/get_employee/$', views.ajax_get_employee, name='ajax_get_employee'),
    url(r'^ajax/get_employee_photo/$', views.ajax_get_employee_photo, name='ajax_get_employee_photo'),
    path('daily-attendance/', views.DailyAttendance, name='daily-attendance'),    
    # url(r'^ajax/delete_employee_schedule_maintenance/$', views.ajax_delete_employee_schedule_maintenance, name='ajax_delete_employee_schedule_maintenance'),

	path('generate-daily-attend/', views.GenerateDailyAttend, name='generate-daily-attend'),
	url(r'^ajax/sp_generate_daily_attend/$', views.ajax_sp_generate_daily_attend, name='ajax_sp_generate_daily_attend'),
	url(r'^ajax/sp_generate_daily_attend_status/$', views.ajax_sp_generate_daily_attend_status, name='ajax_sp_generate_daily_attend_status'),

    path('post-daily-attend/', views.PostDailyAttend, name='post-daily-attend'),
    url(r'^ajax/sp_post_daily_attend/$', views.ajax_sp_post_daily_attend, name='ajax_sp_post_daily_attend'),
    url(r'^ajax/sp_post_daily_attend_progress/$', views.ajax_sp_post_daily_attend_progress, name='ajax_sp_post_daily_attend_progress'),
    url(r'^ajax/check_post_daily_attend_status/$', views.check_post_daily_attend_status, name='ajax_check_post_daily_attend_status'),
    url(r'^ajax/check_post_daily_attend_status_history/$', views.check_post_daily_attend_status_history, name='check_post_daily_attend_status_history'),

	url(r'^ajax/get_attendance_information/$', views.ajax_get_attendance_information, name='ajax_get_attendance_information'),
	url(r'^ajax/delete_employee/$', views.ajax_delete_employee, name='ajax_delete_employee'),

    
    url(r'^ajax/ajax_is_scheduled_between_site/$', views.ajax_is_scheduled_between_site, name='ajax_is_scheduled_between_site'),
    url(r'^ajax/bulk_update_absent_status/$', views.ajax_bulk_update_absent_status, name='ajax_bulk_update_absent_status'),
    url(r'^ajax/get_job_type_list/$', views.ajax_get_job_type_list, name='ajax_get_job_type_list'),


    url(r'^ajax/save_daily_attendance_check_rule_1/$', views.ajax_save_daily_attendance_check_rule_1, name='ajax_save_daily_attendance_check_rule_1'),
    url(r'^ajax/save_daily_attendance/$', views.ajax_save_daily_attendance, name='ajax_save_daily_attendance'),
    url(r'^ajax/save_daily_attendance_cross_site/$', views.ajax_save_daily_attendance_cross_site, name='ajax_save_daily_attendance_cross_site'),

    # Rules
    url(r'^ajax/is_scheduled/$', views.is_scheduled, name='is_scheduled'),
]


# Daily Guard Performance
urlpatterns += [
    path('daily-performance/', views.DailyGuardPerformance, name='daily-guard-performance'),
    path('ajax/search_daily_guard_performance/', views.SearchDailyGurdPerformance, name='search-daily-guard-performance'),
    path('ajax/search_daily_guard_performance_employee_information/', views.SearchDailyGurdPerformanceEmployeeInformation, name='search-daily-guard-performance-employee-information'),
    url(r'^generate-dgp-500/(?P<emp_id>\d+)/(?P<search_date_from>\d{2}/\d{2}/\d{4})/(?P<search_date_to>\d{2}/\d{2}/\d{4})/$', views.generate_dgp_500, name='generate-dgp-500'),
    url(r'^export/xls/$', views.export_dgp_500_xls, name='export_dgp_500_xls'), 
]


# Daily Monitoring Reports
urlpatterns += [
    # path('daily-monitoring-reports/', views.DailyMonitoringReports, name='daily-monitoring-reports'),
    # url(r'^export/xls/$', views.export_dgp_500_xls, name='export_dgp_500_xls'),    
]


# Post Daily Attend
urlpatterns += [
    # url(r'^(?P<task_id>[\w-]+)/$', views.get_progress, name='task_status')
    re_path(r'^celery-progress/', include('celery_progress.urls')),  # the endpoint is configurable
]

