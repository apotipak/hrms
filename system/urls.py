from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index, name='index'),
    path('company-approve-priority', views.CompanyApprovePriorityListView.as_view(), name='company-approve-priority'),
    path('company-approve-priority/<int:pk>', views.CompanyApprovePriorityDetailView.as_view(), name='company-approve-priority_detail'),
    path('company-company-information', views.CompanyInformation, name='company-company-information'),
]
