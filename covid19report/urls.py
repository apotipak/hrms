from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('dashboard/', views.Dashboard, name='dashboard'),

    path('report-by-person/', views.ViewCovid19Report, name='view_covid_19_report'),
    path('ajax-covid-19-report/', views.AjaxCovid19Report, name='ajax-covid-19-report'),

    path('report-by-status/', views.ViewCovid19ReportByStatus, name='view_covid_19_report_by_status'),
    path('ajax-report-by-status/', views.AjaxReportByStatus, name='ajax-report-by-status'),

    path('report-by-latest-status/', views.ViewReportByLatestStatus, name='report-by-latest-status'),
    path('ajax-report-by-latest-status/', views.AjaxReportByLatestStatus, name='ajax-report-by-latest-status'),

    url(r'^download-pdf/(?P<emp_id>\d+)/(?P<get_vaccine_status_option>\w+)/$', views.download_pdf, name='download-pdf'),
]
