from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.CustomerList, name='customer-list'),
    url(r'^customer-dashboard/', views.CustomerDashboard, name='customer-dashboard'),
    path('customer/create', views.CustomerCreate, name='customer-create'),
    path('customer/<int:pk>/update', views.CustomerUpdate, name='cus-main-update'),
   	path('customer/<int:pk>/delete', views.CustomerDelete, name='customer-delete'),
]

urlpatterns += [
  path('performance-information/', views.PerformanceInformation, name='performance-information'),
	path('customer-report/', views.CustomerReport, name='customer-report'),
]

urlpatterns += [    
  url(r'^ajax/get_district_list/$', views.get_district_list, name='get_district_list'),
  url(r'^ajax/get_district_list_modal/$', views.get_district_list_modal, name='get_district_list_modal'),
  url(r'^ajax/get_country/$', views.get_country, name='get_country'),
]

urlpatterns += [
  url(r'^ajax/update_cus_main/$', views.update_cus_main, name='update_cus_main'),
  url(r'^ajax/update_cus_site/$', views.update_cus_site, name='update_cus_site'),
  url(r'^ajax/update_cus_bill/$', views.update_cus_bill, name='update_cus_bill'),
  url(r'^ajax/update_all_cus_tabs/$', views.update_all_cus_tabs, name='update_all_cus_tabs'),
]

urlpatterns += [
  url(r'^ajax/get_contact/$', views.get_contact, name='get_contact'),
  url(r'^ajax/get_contact_list/$', views.get_contact_list, name='get_contact_list'),
  url(r'^ajax/get_contact_list_modal/$', views.get_contact_list_modal, name='get_contact_list_modal'),  
]

urlpatterns += [
  url(r'^ajax/ajax_check_exist_cus_main/$', views.ajax_check_exist_cus_main, name='ajax_check_exist_cus_main'),
  url(r'^ajax/ajax_check_exist_cus_site/$', views.ajax_check_exist_cus_site, name='ajax_check_exist_cus_site'),
  url(r'^ajax/ajax_check_exist_cus_bill/$', views.ajax_check_exist_cus_bill, name='ajax_check_exist_cus_bill'),
]




