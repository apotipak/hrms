from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('report-by-person/', views.ViewCovid19Report, name='view_covid_19_report'),
    path('ajax-covid-19-report/', views.AjaxCovid19Report, name='ajax-covid-19-report'),

    path('report-by-status/', views.ViewCovid19ReportByStatus, name='view_covid_19_report_by_status'),
]
