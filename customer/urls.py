from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.CustomerList, name='customer-list'),
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
]

urlpatterns += [
  url(r'^ajax/update_cus_main/$', views.update_cus_main, name='update_cus_main'),
  url(r'^ajax/update_cus_site/$', views.update_cus_site, name='update_cus_site'),
]
