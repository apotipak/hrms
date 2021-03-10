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
from os import path


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
	sql += "cnt_eff_to, cnt_zone, nosupD, supD, nosupN, supN, Sun, Mon, Tue, Wed, Thu, Fri, Sat, Pub, dept_sht "
	sql += "from V_Contract_Summary "
	sql += "where cnt_id>=" + str(contract_number_from) + " " 
	sql += "and cnt_id<=" + str(contract_number_to) + " "

	print("contract_status:", contract_status)
	if contract_status == "1":
		sql += " and cnt_active=1 "
	elif contract_status == "2":
		sql += " and cnt_active=0 "

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
	
	total_sun = 0
	total_mon = 0
	total_tue = 0
	total_wed = 0
	total_thu = 0
	total_fri = 0
	total_sat = 0	
	total_pub = 0

	total_supD = 0
	total_supN = 0

	total_nosupD = 0
	total_nosupN = 0

	grand_total_sup_DN = 0
	grand_total_nosup_DN = 0
	grand_grand_total = 0

	for row in contract_obj:
		if row[3] is not None:
			cnt_sign_frm = row[3].strftime("%d-%b-%Y")
		else:
			cnt_sign_frm = ""

		if row[4] is not None:
			cnt_sign_to = row[4].strftime("%d-%b-%Y")
		else:
			cnt_sign_to = ""

		if row[5] is not None:
			cnt_eff_frm = row[5].strftime("%d-%b-%Y")
		else:
			cnt_eff_frm = ""

		if row[6] is not None:
			cnt_eff_to = row[6].strftime("%d-%b-%Y")
		else:
			cnt_eff_to = ""

		total_sup_DN = row[9] + row[11]
		total_nosup_DN = row[8] + row[10]
		grand_total = total_sup_DN + total_nosup_DN

		total_supD += row[9]
		total_supN += row[11]
		total_nosupD += row[8]
		total_nosupN += row[10]

		total_sun += row[12]
		total_mon += row[13]
		total_tue += row[14]
		total_wed += row[15]
		total_thu += row[16]
		total_fri += row[17]
		total_sat += row[18]
		total_pub += row[19]

		grand_total_sup_DN += total_sup_DN
		grand_total_nosup_DN += total_nosup_DN
		grand_grand_total += grand_total

		record = {
			"cnt_id": row[0],					
			"cus_name_en": row[1],
			"cus_name_th": row[2],
			"cnt_sign_frm": cnt_sign_frm,
			"cnt_sign_to": cnt_sign_to,
			"cnt_eff_frm": cnt_eff_frm,
			"cnt_eff_to": cnt_eff_to,
			"cnt_zone": row[7],
			"dept_sht": row[20],
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
		"total_sun": total_sun,
		"total_mon": total_mon,
		"total_tue": total_tue,
		"total_wed": total_wed,
		"total_thu": total_thu,
		"total_fri": total_fri,
		"total_sat": total_sat,
		"total_pub": total_pub,

		"total_supD": total_supD,
		"total_supN": total_supN,
		"total_nosupD": total_nosupD,
		"total_nosupN": total_nosupN,

		"grand_total_sup_DN": grand_total_sup_DN,
		"grand_total_nosup_DN": grand_total_nosup_DN,
		"grand_grand_total": grand_grand_total,
	})

	response.status_code = 200
	return response


@permission_required('contractreport.can_access_contract_list_report', login_url='/accounts/login/')
def generate_contract_list(request, *args, **kwargs):    

	base_url = MEDIA_ROOT + '/contract/template/'
	contract_number_from = kwargs['contract_number_from']
	contract_number_to = kwargs['contract_number_to']
	contract_status = kwargs['contract_status']
	contract_zone = kwargs['contract_zone']

	# now = datetime.datetime.now()
	# html = "<html><body>It is now %s.</body></html>" % now
	# return HttpResponse(html)
	
	template_name = base_url + 'CNT_ContractStatus.docx'
	file_name = "contract_list_report"

	context = {
	    'customer': "TEST",
	}

	tpl = DocxTemplate(template_name)
	tpl.render(context)
	tpl.save(MEDIA_ROOT + '/contract/download/' + file_name + ".docx")

	# docx2pdf
	docx_file = path.abspath("media\\contract\\download\\" + file_name + ".docx")
	pdf_file = path.abspath("media\\contract\\download\\" + file_name + ".pdf")    
	convert(docx_file, pdf_file)

	return FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')	


