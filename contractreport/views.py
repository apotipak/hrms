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


@login_required(login_url='/accounts/login/')
def export_contract_list(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Contract_List.xls"'

	r_d500_obj = []
	pickup_record = []
	context = {}
	emp_id = ""
	fname = ""
	cnt_id = ""
	dly_date = ""
	shf_desc = ""
	sch_rank = ""
	pay_type = ""
	bas_amt = ""
	bon_amt = ""
	pub_amt = ""
	otm_amt = ""
	dof = ""
	spare = ""
	tel_amt = ""
	wage_id = ""
	shf_amt_hr = ""
	ot_hr_amt = ""
	absent = ""
	sum_otm_amt = 0
	sum_shf_amt_hr = 0
	sum_bas_amt = 0
	sum_ot_hr_amt = 0
	sum_bon_amt = 0
	sum_pub_amt = 0
	sum_tel_amt = 0
	sum_dof = 0
	sum_spare = 0

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('DGP_500')

	sql = "select "
	sql += "0 as col0, "
	sql += "R_D500.CNT_ID, R_D500.DLY_DATE, 3 as col3, R_D500.SHF_DESC, R_D500.OTM_AMT, R_D500.SHF_AMT_HR,"
	sql += "R_D500.BAS_AMT, R_D500.OT_HR_AMT, R_D500.BON_AMT, R_D500.PUB_AMT, R_D500.TEL_AMT,"
	sql += "R_D500.DOF, R_D500.SPARE, R_D500.WAGE_ID, R_D500.PAY_TYPE, R_D500.EMP_ID,"
	sql += "R_D500.FNAME, R_D500.SCH_RANK, R_D500.ABSENT "
	sql += "FROM HRMS.dbo.R_D500 R_D500 "
	sql += "ORDER BY R_D500.EMP_ID ASC"
	# print("SQL: ", sql)
	try:
		cursor = connection.cursor()
		cursor.execute(sql)
		r_d500_obj = cursor.fetchall()
	finally:
		cursor.close()

	if r_d500_obj is not None:
		if len(r_d500_obj)>0:
			emp_id = r_d500_obj[0][16]
			fullname_th = r_d500_obj[0][17]
			sch_rank = r_d500_obj[0][18]
			search_date_from = r_d500_obj[0][2].strftime('%d/%m/%Y')
			search_date_to = r_d500_obj[len(r_d500_obj)-1][2].strftime('%d/%m/%Y')
			

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	# First Row, First Column
	font_style = xlwt.easyxf('font: bold 1,height 280;')
	ws.write(1, 5, "Daily Guard Performance", font_style)

	font_style = xlwt.XFStyle()
	font_style = xlwt.easyxf('font: height 180;')
	ws.write(3, 0, "Employee ID : " + str(emp_id))
	ws.write(4, 0, "Employee Name : " + str(fullname_th))
	ws.write(5, 0, "Employee Rank : " + str(sch_rank))

	ws.write(2, 14, "From Date : " + str(search_date_from))
	ws.write(3, 14, "To Date : " + str(search_date_to))	
	ws.write(4, 14, "Print Date : " + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M')))

	ws.col(1).width = int(13*260)
	ws.col(3).width = int(10*260)
	ws.col(4).width = int(25*260)
	ws.col(15).width = int(10*260)

	columns = ['', 'CONTRACT', 'DATE', 'DAY', 'SHIFT', 'OT', 'HOURS', 'BAS', 'GOT', 'BON', 'PUB', 'TEL', 'DOF', 'SPARE', 'WAGE', 'PAY TYPE', 'REMARK']
	for col_num in range(len(columns)):
		ws.write(7, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()
	font_style = xlwt.easyxf('font: height 180;')

	# Sheet header, first row
	row_num = 8
	counter = 1

	for row in r_d500_obj:
		number = counter
		fname = row[17]
		cnt_id = str(row[2])
		dly_date = str(row[2].strftime("%d/%m/%Y"))		
		dly_date_week_day = datetime.datetime.strptime(dly_date, '%d/%m/%Y').strftime('%a')
		# print("dly_date_week_day:", dly_date_week_day)
		dly_date_str = str(dly_date)
		shf_desc = row[4]
		sch_rank = row[18]
		pay_type = row[15]

		if row[5] is not None:
			otm_amt = row[5]
		else:
			otm_amt = 0

		if pay_type!="LWO":			
			sum_otm_amt += otm_amt
			
		shf_amt_hr = row[6]
		if pay_type!="LWO":
			sum_shf_amt_hr += shf_amt_hr

		if row[7] is not None:
			bas_amt = row[7]
		else:
			bas_amt = 0
		sum_bas_amt += bas_amt

		if row[8] is not None:
			ot_hr_amt = row[8]
		else:
			ot_hr_amt = 0
		sum_ot_hr_amt += ot_hr_amt

		if row[9] is not None:
			bon_amt = row[9]
		else:
			bon_amt = 0
		sum_bon_amt += bon_amt

		if row[10] is not None:
			pub_amt = row[10]
		else:
			pub_amt = 0
		sum_pub_amt += pub_amt
		
		if row[11] is not None:
			tel_amt = row[11]
		else:
			tel_amt = 0
		sum_tel_amt += tel_amt

		if row[12] is not None:
			dof = row[12]
		else:
			dof = 0
		sum_dof += dof

		spare = row[13]
		sum_spare += spare

		wage_id = row[13]					
		absent = row[19]
		
		for col_num in range(len(row)):
			if(col_num==0):
				ws.write(row_num, 0, counter, font_style)
			elif(col_num==2):
				ws.write(row_num, 2, dly_date_week_day.upper(), font_style)
			elif(col_num==3):
				ws.write(row_num, 3, dly_date_str, font_style)
			elif (col_num==16) or (col_num==17) or (col_num==18) or (col_num==19):
				ws.write(row_num, col_num, "", font_style)
			else:
				ws.write(row_num, col_num, row[col_num], font_style)

		row_num += 1
		counter += 1

	# Sum
	font_style = xlwt.XFStyle()
	font_style = xlwt.easyxf('font: height 180;')
	
	font_style.font.bold = True
	for col_num in range(len(row)):
		if(col_num==0):
			ws.write(row_num, 0, counter-1, font_style)
		elif(col_num==1):
			ws.write(row_num, 1, "Days", font_style)			
		elif(col_num==5):
			ws.write(row_num, 5, sum_otm_amt, font_style)
		elif(col_num==6):
			ws.write(row_num, 6, sum_shf_amt_hr, font_style)
		elif(col_num==7):
			ws.write(row_num, 7, sum_bas_amt, font_style)
		elif(col_num==8):
			ws.write(row_num, 8, sum_ot_hr_amt, font_style)
		elif(col_num==9):
			ws.write(row_num, 9, sum_bon_amt, font_style)
		elif(col_num==10):
			ws.write(row_num, 10, sum_pub_amt, font_style)
		elif(col_num==11):
			ws.write(row_num, 11, sum_tel_amt, font_style)			
		elif(col_num==12):
			ws.write(row_num, 12, sum_dof, font_style)
		elif(col_num==13):
			ws.write(row_num, 13, sum_spare, font_style)

	wb.save(response)
	return response
