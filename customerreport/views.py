from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils import translation
from django.utils.translation import ugettext as _
import django.db as db
from django.db import connection
from page.rules import *
from django.utils import timezone


@permission_required('customerreport.can_access_export_customer_address_main_report', login_url='/accounts/login/')
def ExportCustomerAddressMainReport(request):
    template_name = 'contract/contract_create.html'
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    today_date = settings.TODAY_DATE
    response_data = dict()

    if request.method == "POST":
        if form.is_valid():          
            response_data['form_is_valid'] = True            
        else:            
            response_data['form_is_valid'] = False

        return JsonResponse(response_data)     
    else:
        print("GET: contract_create()")
        
    return render(request, 'customerreport/export_customer_address_main_report.html', 
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
        })


def todo():
    sql = "SELECT cus_id, cus_name_th, cus_add1_th, cus_add2_th, cus_subdist_th, cus_name_en, cus_add1_en, cus_add2_en, cus_subdist_en, cus_zip, cus_tel, "
    sql += "cus_fax, cus_email, cus_active, con_fname_th, con_lname_th, con_position_th, con_fname_en, con_lname_en, con_position_en, dist_th, dist_en, city_en, city_th, dept_en "
    sql += "FROM EX_MAIN EX_MAIN WHERE cus_active = 1;"

