from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [    
    path('', views.ScheduleMaintenance, name='schedule-maintenance'),
    url(r'^ajax/get_customer/$', views.ajax_get_customer, name='ajax_get_customer'),
    url(r'^ajax/get_customer_schdule_plan_list/$', views.ajax_get_customer_schedule_plan_list, name='ajax_get_customer_schedule_plan_list'),
    url(r'^ajax/get_customer_schdule_plan/$', views.ajax_get_customer_schedule_plan, name='ajax_get_customer_schedule_plan'),
    url(r'^ajax/save_customer_schdule_plan/$', views.ajax_save_customer_schedule_plan, name='ajax_save_customer_schedule_plan'),
    
    url(r'^ajax/get_employee_list/$', views.ajax_get_employee_list, name='ajax_get_employee_list'),
    # url(r'^ajax/get_contact_list/$', views.get_contact_list, name='get_contact_list'),
]