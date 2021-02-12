from django.urls import path, include
from django.conf.urls import url
from . import views

from system import helper
from django.views.generic import RedirectView


urlpatterns = [
    # path('', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    path('user-profile', views.userprofile, name='user-profile'),    
    path('user-password', views.userpassword, name='user-password'),
    path('user-language', views.userlanguage, name='user-language'),

    path('open-car-form-page', views.openCarFormPage, name='open-car-form-page'),    
    path('open-car-form', helper.openCarForm, name='open-car-form'),
]
