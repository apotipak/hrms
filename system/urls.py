from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index, name='index'),
]

"""Company / Approve Priority"""
urlpatterns += [
    path('company-approve-priority', views.CompanyApprovePriorityListView.as_view(), name='company-approve-priority'),
    path('company-approve-priority/<int:pk>', views.CompanyApprovePriorityDetailView.as_view(), name='company-approve-priority-detail'),
    path('company-approve-priority/create', views.CompanyApprovePriorityCreate, name='company-approve-priority-create'),
    path('company-approve-priority/<int:pk>/update', views.CompanyApprovePriorityUpdate, name='company-approve-priority-update'),
   	path('company-approve-priority/<int:pk>/delete', views.CompanyApprovePriorityDelete, name='company-approve-priority-delete'),
]

"""Company / Company Information """
urlpatterns += [
    path('company-company-information', views.CompanyInformation, name='company-company-information'),
]

