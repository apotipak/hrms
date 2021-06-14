from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.ViewCovid19Report, name='view_covid_19_report'),
    path('ajax-covid-19-report/', views.AjaxCovid19Report, name='ajax-covid-19-report'),
]
