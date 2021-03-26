from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.static import serve
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils import translation
from django.utils.translation import ugettext as _
import django.db as db
from django.db import connection
from page.rules import *
import datetime
from django.utils import timezone
from system.models import ComZone
from django.http import JsonResponse
from hrms.settings import MEDIA_ROOT
from django.http import FileResponse
from docxtpl import DocxTemplate
from docx2pdf import convert
import xlwt
from os import path


@permission_required('dailyattendreport.can_access_gpm403_daily_guard_performance_by_contract_report', login_url='/accounts/login/')
def GPM403DailyGuardPerformanceReport(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    
    today_date = settings.TODAY_DATE.strftime("%d/%m/%Y")
    contract_number_from = request.POST.get('contract_number_from')
    contract_number_to = request.POST.get('contract_number_to')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    contract_number_from = 0 if contract_number_from is None else contract_number_from
    contract_number_to = 9999999999 if contract_number_to is None else contract_number_to
    start_date = today_date if start_date is None else datetime.datetime.strptime(start_date, "%d/%m/%Y").date()
    end_date = today_date if end_date is None else datetime.datetime.strptime(end_date, "%d/%m/%Y").date()

    '''
    print("today_date = ", today_date)
    print("contract_number_from = ", contract_number_from)
    print("contract_number_to = ", contract_number_to)
    print("start_date = ", start_date)
    print("end_date = ", end_date)
    '''

    return render(request, 'dailyattendreport/gpm403_daily_guard_performance_by_contract_report.html',
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version,
        'db_server': db_server, 
        'today_date': today_date,
        'start_date': start_date,
        'end_date': end_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
        'is_error': False,
        'dly_plan_list': None,
        })


@permission_required('dailyattendreport.can_access_gpm403_daily_guard_performance_by_contract_report', login_url='/accounts/login/')
def AjaxGPM403DailyGuardPerformanceReport(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    
    today_date = settings.TODAY_DATE.strftime("%d/%m/%Y")
    contract_number_from = request.POST.get('contract_number_from')
    contract_number_to = request.POST.get('contract_number_to')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    contract_number_from = 0 if contract_number_from is None else contract_number_from
    contract_number_to = 9999999999 if contract_number_to is None else contract_number_to
    start_date = today_date if start_date is None else datetime.datetime.strptime(start_date, "%d/%m/%Y").date()
    end_date = today_date if end_date is None else datetime.datetime.strptime(end_date, "%d/%m/%Y").date()

    sql = "select emp_fname_th, emp_lname_th, shf_desc, dept_en, cnt_id, "
    sql += "emp_id, dly_date, sch_shift, dept_id, sch_rank, "
    sql += "absent, relieft_id, tel_man, tel_paid, ot, "
    sql += "ot_hr_amt, cus_name_th, late, late_full "
    sql += "FROM V_HDLYPLAN "
    sql += "WHERE absent = 0 AND (sch_shift <> 99 OR sch_shift <> 999) "
    sql += "and (cnt_id>=" + str(contract_number_from) + " and cnt_id<=" + str(contract_number_to) + ") "
    sql += "and (dly_date>='" + str(start_date) + "' and dly_date<='" + str(end_date) + "') "
    sql += "ORDER BY cnt_id ASC, dly_date ASC, shf_desc ASC, emp_id ASC"
    print(sql)
    
    dly_plan_obj = None
    record = {}
    dly_plan_list = []
    error_message = ""

    try:                
        cursor = connection.cursor()
        cursor.execute(sql)
        dly_plan_obj = cursor.fetchall()        
    except db.OperationalError as e:
        error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
    except db.Error as e:
        error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
    finally:
        cursor.close()

    if dly_plan_obj is not None:
        if len(dly_plan_obj)>0:           
            for item in dly_plan_obj:             
                record = {
                    "emp_fname_th": item[0],
                    "emp_lname_th": item[1],
                    "shf_desc": item[2],
                    "dept_en": item[3],
                    "cnt_id": item[4],
                    "emp_id": item[5],
                    "dly_date": item[6].strftime("%d/%m/%Y"),
                    "sch_shift": item[7],
                    "dept_id": item[8],
                    "sch_rank": item[9],
                    "absent": item[10],
                    "relieft_id": item[11],
                    "tel_man": item[12],
                    "tel_paid": item[13],
                    "ot": item[14],
                    "ot_hr_amt": item[15],
                    "cus_name_th": item[16],
                    "late": item[17],
                    "late_full": item[18],
                }
                dly_plan_list.append(record)

    response = JsonResponse(data={        
        "is_error": False,
        "error_message": error_message,
        "dly_plan_list": list(dly_plan_list),
    })

    response.status_code = 200
    return response
