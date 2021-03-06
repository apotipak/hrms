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

def dept_sht_text_display(dept_sht):
	dept_sht_text = str(dept_sht)

	dept_sht_text = dept_sht_text.replace("Zone", "")
	dept_sht_text = dept_sht_text.replace("ZONE ", "")
	dept_sht_text = dept_sht_text.replace("SGD.", "")
	dept_sht_text = dept_sht_text.replace("SP-", "")

	return dept_sht_text


def AJAXReportSearchContract(request):
	is_error = False
	error_message = "No error"
	contract_number_from = request.POST.get('contract_number_from')
	contract_number_to = request.POST.get('contract_number_to')
	contract_status = request.POST.get('contract_status')
	contract_zone = request.POST.get('contract_zone')
	contract_list = []

	sql = "select cnt_id, cus_name_en, cus_name_th, "
	sql += "cnt_sign_frm, cnt_sign_to, cnt_eff_frm, "
	sql += "cnt_eff_to, cnt_zone, nosupD, supD, nosupN, supN, Sun, Mon, Tue, Wed, Thu, Fri, Sat, Pub, dept_sht "
	sql += "from V_Contract_Summary "
	sql += "where cnt_id>=" + str(contract_number_from) + " " 
	sql += "and cnt_id<=" + str(contract_number_to) + " "
	print("TEST ", sql)
	
	if contract_status == "1":
		sql += " and cnt_active=1 "
	elif contract_status == "2":
		sql += " and cnt_active=0 "

	if contract_zone != "":
		sql += " and cnt_zone=" + contract_zone + " "
	else:
		sql += " "

	sql += "ORDER BY cnt_id;"

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


	today_date = datetime.datetime.now().strftime("%Y-%m-%d")
	print("DEBUG: today date = ", today_date)

	for row in contract_obj:
		if row[3] is not None:
			cnt_sign_frm = row[3].strftime("%d-%b-%Y")
		else:
			cnt_sign_frm = ""

		if row[4] is not None:
			if row[4].strftime("%Y-%m-%d") == "2999-12-31":
				cnt_sign_to = "<div class='text-left text-info'><i>Open ended</i></div>"
			else:
				cnt_sign_to = row[4].strftime("%d-%b-%Y")
				if datetime.datetime.now() > row[4]:
					cnt_sign_to = "<div class='text-left text-danger'>" + str(cnt_sign_to) + "</div>"
				else:
					cnt_sign_to = "<div class='text-left'>" + str(cnt_sign_to) + "</div>"
		else:
			cnt_sign_to = "<div class='text-left text-info'><i>Open ended</i></div>"


		if row[5] is not None:
			cnt_eff_frm = row[5].strftime("%d-%b-%Y")
		else:
			cnt_eff_frm = ""

		if row[6] is not None:
			if row[6].strftime("%Y-%m-%d") == "2999-12-31":
				cnt_eff_to = "<div class='text-left text-info'><i>Open ended</i></div>"
			else:				
				cnt_eff_to = row[6].strftime("%d-%b-%Y")
				if datetime.datetime.now() > row[6]:
					cnt_eff_to = "<div class='text-left text-danger'>" + str(cnt_eff_to) + "</div>"
				else:
					cnt_eff_to = "<div class='text-left'>" + str(cnt_eff_to) + "</div>"
		else:
			cnt_eff_to = "<div class='text-left text-info'><i>Open ended</i></div>"

		# print("|" + row[20].strip() + "|")
		
		'''
		if (contract_zone=="2050") or (row[20].strip()=='SP'):
			dept_sht_text = "A"
		else:
			dept_sht_text = dept_sht_text_display(row[20])
		'''	
		dept_sht_text = zone_name_display_text(row[7])

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
			"dept_sht": dept_sht_text,
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


@login_required(login_url='/accounts/login/')
def export_contract_list_report(request, *args, **kwargs):

	base_url = MEDIA_ROOT + '/contract/template/'
	contract_number_from = kwargs['contract_number_from']
	contract_number_to = kwargs['contract_number_to']
	contract_status = kwargs['contract_status']
	contract_zone = kwargs['contract_zone']

	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Contract_List.xls"'

	customer_list_obj = []
	pickup_record = []
	context = {}

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Contract List')

	sql = "select cnt_id, cus_name_en, cus_name_th, "
	sql += "cnt_sign_frm, cnt_sign_to, cnt_eff_frm, "
	sql += "cnt_eff_to, cnt_zone, nosupD, supD, nosupN, supN, Sun, Mon, Tue, Wed, Thu, Fri, Sat, Pub, dept_sht "
	sql += "from V_Contract_Summary "
	sql += "where cnt_id>=" + str(contract_number_from) + " " 
	sql += "and cnt_id<=" + str(contract_number_to) + " "

	if contract_status == "1":
		sql += " and cnt_active=1 "
	elif contract_status == "2":
		sql += " and cnt_active=0 "
	else:
		sql += " "		

	if contract_zone != "":
		if contract_zone == "all_zone":
			sql += " "
		else: 
			sql += " and cnt_zone=" + contract_zone + " "

	sql += "ORDER BY cnt_id;"

	print("SQL1:", sql)

	try:
		cursor = connection.cursor()
		cursor.execute(sql)
		customer_list_obj = cursor.fetchall()
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

	# TITLE
	print("contract_zone value = ", contract_zone)
	if contract_zone=="all_zone":
		title_header = "Contract List : All Zones"
	else:
		sql = "select zone_en from com_zone where zone_id=" + str(contract_zone) + ";"
		try:
			with connection.cursor() as cursor:     
				cursor.execute(sql)
				com_zone_obj = cursor.fetchone()

			if com_zone_obj is not None:				
				if com_zone_obj[0] is None:
					title_header = "Contract List : Unknown zone"
				else:
					title_header = "Contract List : " + com_zone_obj[0]
			else:
				title_header = "Contract List : Unknown zone"

		except db.OperationalError as e:
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
		except db.Error as e:
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
		finally:
			cursor.close()
	

	font_style = xlwt.XFStyle()
	# font_style.font.bold = True
	font_style = xlwt.easyxf('font: bold 1,height 280;')
	ws.write(0, 0, title_header, font_style)

	# COLUMN WIDTH
	ws.col(0).width = int(5*260)
	ws.col(1).width = int(15*260)
	ws.col(2).width = int(50*260)
	ws.col(3).width = int(50*260)
	ws.col(19).width = int(11*260)
	ws.col(19).width = int(12*260)
	ws.col(20).width = int(12*260)
	ws.col(21).width = int(12*260)
	ws.col(22).width = int(12*260)
	ws.col(23).width = int(12*260)
	
	# COLUMN NAME
	font_style = xlwt.XFStyle()
	font_style = xlwt.easyxf('font: bold 1, height 180;')	
	font_style = xlwt.easyxf('font: bold 1, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; align: vert centre, horiz centre;')
	# font_style = xlwt.easyxf("align: vert centre, horiz centre")

	columns = ['NO.', 'CONTRACT ID', 'SITE NAME (TH)', 'SITE NAME (EN)', 'ZONE', 'DAY', 'SO', 'SUP', 'TOTAL', 'CONTRACT DATE', 'EFFECTIVE DATE']
	for col_num in range(len(columns)):	
		if(col_num==0):
			ws.write_merge(2, 3, 0, 0, columns[col_num], font_style)
		elif(col_num==1):			
			ws.write_merge(2, 3, 1, 1, columns[col_num], font_style)
		elif(col_num==2):			
			ws.write_merge(2, 3, 2, 2, columns[col_num], font_style)			
		elif(col_num==3):			
			ws.write_merge(2, 3, 3, 3, columns[col_num], font_style)
		elif(col_num==4):
			ws.write_merge(2, 3, 4, 4, columns[col_num], font_style)

		# Zone
		elif(col_num==4):
			ws.write_merge(2, 2, 5, 5, columns[col_num], font_style)

		# Day
		elif(col_num==5):			
			ws.write_merge(2, 2, 5, 12, columns[col_num], font_style)
		
		# SO
		elif(col_num==6):
			ws.write_merge(2, 2, 13, 15, columns[col_num], font_style)

		# SUP
		elif(col_num==7):
			ws.write_merge(2, 2, 16, 18, columns[col_num], font_style)
		
		# TOTAL
		elif(col_num==8):						
			ws.write_merge(2, 3, 19, 19, columns[col_num], font_style)

		# Contract Date
		elif(col_num==9):
			ws.write_merge(2, 2, 20, 21, columns[col_num], font_style)
		
		# Effective Date
		elif(col_num==10):
			ws.write_merge(2, 2, 22, 23, columns[col_num], font_style)			
		else:
			message = ""

	ws.write(3, 5, "MO", font_style)
	ws.write(3, 6, "TU", font_style)
	ws.write(3, 7, "WE", font_style)
	ws.write(3, 8, "TH", font_style)
	ws.write(3, 9, "FR", font_style)
	ws.write(3, 10, "SA", font_style)
	ws.write(3, 11, "SU", font_style)
	ws.write(3, 12, "PU", font_style)

	ws.write(3, 13, "D", font_style)
	ws.write(3, 14, "N", font_style)
	ws.write(3, 15, "TOTAL", font_style)
	
	ws.write(3, 16, "D", font_style)
	ws.write(3, 17, "N", font_style)
	ws.write(3, 18, "TOTAL", font_style)
	
	ws.write(3, 20, "FROM", font_style)
	ws.write(3, 21, "TO", font_style)
	ws.write(3, 22, "FROM", font_style)
	ws.write(3, 23, "TO", font_style)




	if customer_list_obj is not None:
		if len(customer_list_obj) > 0:
			# font_style = xlwt.XFStyle()
			# font_style = xlwt.easyxf('font: height 180;')
			row_num = 4
			counter = 1

			for row in customer_list_obj:
				row_count = counter
				cnt_id = row[0]
				cus_name_en = row[1]
				cus_name_th = row[2]
				
				# cnt_zone = row[7]			
				'''
				if (contract_zone=="2050") or (row[20].strip())=='SP':
					dept_sht_text = "A"
				else:
					dept_sht_text = dept_sht_text_display(row[20])
				'''
				dept_sht_text = zone_name_display_text(row[7])

				cnt_sign_frm = "" if row[3] is None else str(row[3].strftime("%d/%m/%Y"))
				cnt_sign_to = "" if row[4] is None else str(row[4].strftime("%d/%m/%Y"))
				cnt_eff_frm = "" if row[5] is None else str(row[5].strftime("%d/%m/%Y"))				
				cnt_eff_to = "" if row[6] is None else str(row[6].strftime("%d/%m/%Y"))
				
				sun = row[12]
				mon = row[13]
				tue = row[14]
				wed = row[15]
				thu = row[16]
				fri = row[17]
				sat = row[18]
				pub = row[19]

				nosupD = row[8]
				supD = row[9]
				nosupN = row[10]
				supN = row[11]


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

				# font_style = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; align: vert centre, horiz centre;')
				font_style = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')

				for col_num in range(24):
					if(col_num==0):
						ws.write(row_num, 0, row_count, font_style)
					elif(col_num==1):
						ws.write(row_num, 1, cnt_id, font_style)			
					elif(col_num==2):
						# font_style = xlwt.easyxf('font: height 200;')
						ws.write(row_num, 2, cus_name_th, font_style)
					elif(col_num==3):
						ws.write(row_num, 3, cus_name_en, font_style)
					elif(col_num==4):
						ws.write(row_num, 4, dept_sht_text, font_style)
					elif(col_num==5):
						ws.write(row_num, 5, mon, font_style)
					elif(col_num==6):
						ws.write(row_num, 6, tue, font_style)
					elif(col_num==7):
						ws.write(row_num, 7, wed, font_style)
					elif(col_num==8):
						ws.write(row_num, 8, thu, font_style)						
					elif(col_num==9):
						ws.write(row_num, 9, fri, font_style)			
					elif(col_num==10):
						ws.write(row_num, 10, sat, font_style)
					elif(col_num==11):
						ws.write(row_num, 11, sun, font_style)
					elif(col_num==12):
						ws.write(row_num, 12, pub, font_style)
					elif(col_num==13):
						ws.write(row_num, 13, nosupD, font_style)
					elif(col_num==14):
						ws.write(row_num, 14, nosupN, font_style)
					elif(col_num==15):
						ws.write(row_num, 15, total_nosup_DN, font_style)
					elif(col_num==16):
						ws.write(row_num, 16, supD, font_style)
					elif(col_num==17):
						ws.write(row_num, 17, supN, font_style)
					elif(col_num==18):
						ws.write(row_num, 18, total_sup_DN, font_style)
					elif(col_num==19):
						ws.write(row_num, 19, grand_total, font_style)
					elif(col_num==20):
						ws.write(row_num, 20, cnt_sign_frm, font_style)
					elif(col_num==21):
						ws.write(row_num, 21, cnt_sign_to, font_style)
					elif(col_num==22):
						ws.write(row_num, 22, cnt_eff_frm, font_style)
					elif(col_num==23):
						ws.write(row_num, 23, cnt_eff_to, font_style)

				# font_style = xlwt.easyxf('font: height 180;')
				row_num += 1
				counter += 1

			# font_style = xlwt.easyxf("align: vert centre, horiz centre")
		else:
			message = ""

		# Add TOTAL row
		
		# font_style = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; align: vert centre, horiz centre;')
		# font_style = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; align: vert centre, horiz centre;')
		ws.write(row_num, 5, total_mon, font_style)
		ws.write(row_num, 6, total_tue, font_style)
		ws.write(row_num, 7, total_wed, font_style)
		ws.write(row_num, 8, total_thu, font_style)
		ws.write(row_num, 9, total_fri, font_style)
		ws.write(row_num, 10, total_sat, font_style)
		ws.write(row_num, 11, total_sun, font_style)
		ws.write(row_num, 12, total_pub, font_style)

		ws.write(row_num, 13, total_nosupD, font_style)
		ws.write(row_num, 14, total_nosupN, font_style)
		ws.write(row_num, 15, grand_total_nosup_DN, font_style)

		ws.write(row_num, 16, total_supD, font_style)
		ws.write(row_num, 17, total_supN, font_style)
		ws.write(row_num, 18, grand_total_sup_DN, font_style)

		ws.write(row_num, 19, grand_grand_total, font_style)

		font_style = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; align: vert centre, horiz centre;')
		ws.write_merge(row_num, row_num, 0, 4, "TOTAL", font_style)
	else:
		message = ""
	  
	
	wb.save(response)
	return response	