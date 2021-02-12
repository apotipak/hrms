from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from employee.models import Employee, EmpPhoto
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from .forms import ChangePasswordForm, LanguageForm
from django.utils import translation
from django.contrib import messages
from django.utils.translation import ugettext as _
from page.rules import *
from base64 import b64encode
import os


@login_required(login_url='/accounts/login/')
def index(request):
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = settings.TODAY_DATE

    if request.user.is_superuser:
        employee_photo = ""
    else:
        if request.user.username!="CMS_SUP":
            employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()   
            employee_photo = b64encode(employee_info.image).decode("utf-8")        
        else:
            employee_info = None
            employee_photo = None

    return render(request, 'index.html', {
    	'project_name': project_name, 
    	'project_version': project_version, 
    	'db_server': db_server, 
    	'today_date': today_date,
        'employee_photo': employee_photo,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
    })


@login_required(login_url='/accounts/login/')
def userprofile(request):
    user_language = getDefaultLanguage(request.user.username)
    translation.activate(user_language)

    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = getDateFormatDisplay(user_language)   

    username = request.user.username
    # employee_profile = Employee.objects.filter(emp_id=username).get()
    employee_profile = get_list_or_404(Employee, emp_id=username)

    return render(request, 'page/user_profile.html', {
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'user_language': user_language,
        'employee_profile': employee_profile,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],        
    })
    

@login_required(login_url='/accounts/login/')
def userpassword(request):
    user_language = getDefaultLanguage(request.user.username)
    translation.activate(user_language)

    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = getDateFormatDisplay(user_language)   

    if request.user.is_superuser:
        employee_photo = ""
    else:
        employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()    
        employee_photo = b64encode(employee_info.image).decode("utf-8")        

    form = ChangePasswordForm(request.POST, user=request.user)
    
    if request.method == "POST":
        if form.is_valid():            
            new_password = form.cleaned_data['new_password']
            u = User.objects.get(username__exact=request.user)
            u.set_password(new_password)
            u.save()            
            # return HttpResponseRedirect('/user-profile')
            return HttpResponseRedirect('/')
    else:
        form = ChangePasswordForm(user=request.user)   

    return render(request, 'page/user_password.html', {
        'form': form,
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'employee_photo': employee_photo,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],        
    })


@login_required(login_url='/accounts/login/')
def userlanguage(request):
    user_language = getDefaultLanguage(request.user.username)
    translation.activate(user_language)

    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = getDateFormatDisplay(user_language)   

    form = LanguageForm(request.POST, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            language_code = form.cleaned_data['language_code']
            username = request.user.username
            userid = request.user.id

            print("language_code = " + str(language_code))

            if not UserProfile.objects.filter(employee_id=username).exists():
                print("debug 1")
                UserProfile.objects.create(language_code=language_code, updated_by_id=userid, employee_id=username)
            else:
                print("debug 2")
                employee = UserProfile.objects.get(employee_id=username)
                employee.language_code = language_code
                employee.updated_by_id = userid
                employee.employee_id = username
                employee.save()
            
            messages.success(request, _('ตั้งค่าใหม่สำเร็จ'))
            return HttpResponseRedirect('/user-language')
    else:
        form = LanguageForm(user=request.user)    

    return render(request, 'page/user_language.html', {
        'form': form,
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],        
    })


def openCarFormPage(request):    
    return render(request, 'page/open_car_form_page.html') 
