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
from system.models import ComZone
from django.http import JsonResponse


@permission_required('contractreport.can_access_contract_list_report', login_url='/accounts/login/')
def ContractListReport(request):
    template_name = 'contract/contract_create.html'
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    today_date = settings.TODAY_DATE
    
    zone_list = ComZone.objects.all().order_by('zone_id')

    return render(request, 'contractreport/contract_list_report.html', 
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
        "zone_list": zone_list,
        })


def AJAXReportSearchContract(request):
	is_error = False
	error_message = "No error"
	contract_number_from = request.POST.get('contract_number_from')
	contract_number_to = request.POST.get('contract_number_to')
	contract_status = request.POST.get('contract_status')
	contract_zone = request.POST.get('contract_zone')
	contract_list = []

	# sql = "select cnt_id, cus_name_th, cus_name_en, cnt_zone from v_cuscontract "
	# sql + = "where cnt_id>=" + str(contract_number_from) + " " 
	# sql += "and cnt_id<=" + str(contract_number_to)

	sql = "select cnt_id, cus_name_en, cus_name_th, "
	sql += "cnt_sign_frm, cnt_sign_to, cnt_eff_frm, "
	sql += "cnt_eff_to, cnt_zone, nosupD, supD, nosupN, supN, Sun, Mon, Tue, Wed, Thu, Fri, Sat, Pub "
	sql += "from V_Contract_Summary "
	sql += "where cnt_id>=" + str(contract_number_from) + " " 
	sql += "and cnt_id<=" + str(contract_number_to) + " "

	if contract_status != "":
		sql += " and cnt_active=" + str(contract_status) + " "

	if contract_zone != "":
		sql += " and cnt_zone=" + contract_zone + " "

	sql += "ORDER BY cnt_id;"

	print("DEBUG sql = ", sql)

	try:
	    with connection.cursor() as cursor:     
	        cursor.execute(sql)
	        contract_obj = cursor.fetchall()

	except db.OperationalError as e:
	    is_error = True
	    error_message = "Error message: " + str(e)
	except db.Error as e:
	    is_error = True
	    error_message = "Error message: " + str(e)
	finally:
	    cursor.close()
	
	for row in contract_obj:
		if row[3] is not None:
			cnt_sign_frm = row[3].strftime("%d/%b/%Y")
		else:
			cnt_sign_frm = ""

		if row[4] is not None:
			cnt_sign_to = row[4].strftime("%d/%b/%Y")
		else:
			cnt_sign_to = ""

		if row[5] is not None:
			cnt_eff_frm = row[5].strftime("%d/%b/%Y")
		else:
			cnt_eff_frm = ""

		if row[6] is not None:
			cnt_eff_to = row[6].strftime("%d/%b/%Y")
		else:
			cnt_eff_to = ""

		total_sup_DN = row[9] + row[11]
		total_nosup_DN = row[8] + row[10]
		grand_total = total_sup_DN + total_nosup_DN

		record = {
			"cnt_id": row[0],					
			"cus_name_en": row[1],
			"cus_name_th": row[2],
			"cnt_sign_frm": cnt_sign_frm,
			"cnt_sign_to": cnt_sign_to,
			"cnt_eff_frm": cnt_eff_frm,
			"cnt_eff_to": cnt_eff_to,
			"cnt_zone": row[7],
			"nosupD": row[8],
			"supD": row[9],
			"nosupN": row[10],
			"supN": row[11],
			"sun": row[12],
			"mon": row[13],
			"tue": row[14],
			"wed": row[15],
			"thu": row[16],
			"fri": row[17],
			"sat": row[18],
			"pub": row[19],
			"total_sup_DN": total_sup_DN,
			"total_nosup_DN": total_nosup_DN,
			"grand_total": grand_total,
			}
		contract_list.append(record)		

	response = JsonResponse(data={        
	    "is_error": is_error,
	    "error_message": error_message,
	    "contract_list": list(contract_list),
	})

	response.status_code = 200
	return response


