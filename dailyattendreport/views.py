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
    print("contract_number_from = ", contract_number_from)
    print("contract_number_to = ", contract_number_to)
    print("start_date = ", start_date)
    print("end_date = ", end_date)


    sql = "select emp_fname_th, emp_lname_th, shf_desc, dept_en, cnt_id, "
    sql += "emp_id, dly_date, sch_shift, dept_id, sch_rank, "
    sql += "absent, relieft_id, tel_man, tel_paid, ot, "
    sql += "ot_hr_amt, cus_name_th, late, late_full "
    sql += "FROM V_HDLYPLAN "
    sql += "WHERE absent = 0 AND (sch_shift <> 99 OR sch_shift <> 999) "
    sql += "and (cnt_id>=1486000001 and cnt_id<=1486000001) "
    sql += "and (dly_date>='2021-02-01' and dly_date<='2021-02-28') "
    sql += "ORDER BY cnt_id ASC, dly_date ASC, shf_desc ASC, emp_id ASC"
    print("SQL : ", sql)

    return render(request, 'dailyattendreport/gpm403_daily_guard_performance_by_contract_report.html',
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
        })
