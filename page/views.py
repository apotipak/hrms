import os
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
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from page.rules import *
from base64 import b64encode
from django.http import JsonResponse
import django.db as db
from django.db import connection
from datetime import datetime


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
        if request.user.username=='CMS_SUP' or request.user.username=='superadmin':
            employee_info = ""
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


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def AjaxSearchEmployeeD1(request):
    # Constant 
    # Force to find D1 only
    emp_type = 'D1'
    
    # Parameter
    emp_id = request.POST.get('search_emp_id')
    emp_fname = request.POST.get('search_emp_firstname')
    emp_lname = request.POST.get('search_emp_lastname')

    # Initial value
    is_error = True
    error_message = ""
    employee_search_list = []

    # TODO
    print(emp_id, " | ", emp_fname, " | ", emp_lname)

    if len(emp_id) > 0:
        # sql = "select emp_id,emp_fname_th, emp_lname_th,emp_rank,emp_status,sts_th from v_employee where emp_type='D1' and emp_id=" + str(emp_id) + ";"
        sql = "select emp_id,emp_fname_th, emp_lname_th,emp_rank,emp_status,sts_th,dept_sht,emp_join_date,emp_term_date from v_employee where emp_type='D1' and emp_id like '" + str(emp_id) + "%';"
    elif emp_fname != "0":
        if emp_lname != "0":
            sql = "select emp_id,emp_fname_th, emp_lname_th,emp_rank,emp_status,sts_th,dept_sht,emp_join_date,emp_term_date from v_employee where emp_type='D1' and emp_fname_th like '" + str(emp_fname)+ "%' and emp_lname_th like '" + str(emp_lname) + "%';"
        else:
            sql = "select emp_id,emp_fname_th, emp_lname_th,emp_rank,emp_status,sts_th,dept_sht,emp_join_date,emp_term_date from v_employee where emp_type='D1' and emp_fname_th like '" + str(emp_fname)+ "%';"
    elif emp_lname != "0":
        sql = "select emp_id,emp_fname_th, emp_lname_th,emp_rank,emp_status,sts_th,dept_sht,emp_join_date,emp_term_date from v_employee where emp_type='D1' and emp_lname_th like '" + str(emp_lname)+ "%';"


    print("SQL : ", sql)

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        employee_search_list = cursor.fetchall()
        is_error = False;
    except db.OperationalError as e:
        error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
    except db.Error as e:
        error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
    finally:
        cursor.close()

    result_list = []
    record = {}
    if employee_search_list is not None:
        if len(employee_search_list) > 0:        
            for item in employee_search_list:
                emp_id = item[0]
                emp_fname_th = item[1]
                emp_lname_th = item[2]
                emp_fullname_th = str(item[1]) + " " + str(item[2])
                emp_rank = item[3]
                emp_status = item[4]
                
                if len(item[5])>=20:
                    sts_th = item[5][0:20]                    
                else:
                    sts_th = item[5]

                dept_sht = item[6]

                if item[7] is not None:
                    emp_join_date = datetime.strptime(str(item[7]), '%Y-%m-%d %H:%M:%S')
                    emp_join_date = emp_join_date.strftime("%d/%m/%Y")
                else:
                    emp_join_date = ""
                

                if item[8] is not None:
                    emp_term_date = datetime.strptime(str(item[8]), '%Y-%m-%d %H:%M:%S')
                    emp_term_date = emp_term_date.strftime("%d/%m/%Y")
                else:
                    emp_term_date = ""

                record = {
                    "emp_id": emp_id,
                    "emp_fname_th": emp_fname_th,
                    "emp_lname_th": emp_lname_th,
                    "emp_fullname_th": emp_fullname_th,
                    "emp_rank": emp_rank,
                    "emp_status": emp_status,
                    "sts_th": sts_th,
                    "dept_sht": dept_sht,
                    "emp_join_date": emp_join_date,
                    "emp_term_date": emp_term_date,
                }
                result_list.append(record)

    response = JsonResponse(data={        
        "is_error": is_error,
        "error_message": error_message,
        "employee_search_list": list(employee_search_list),
        "result_list": result_list,
    })

    response.status_code = 200
    return response
