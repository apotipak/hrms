from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils import translation
from django.utils.translation import ugettext as _
import django.db as db
from django.db import connection
from page.rules import *
from django.utils import timezone
from page.rules import *
from hrms.settings import MEDIA_ROOT
from base64 import b64encode
from docxtpl import DocxTemplate
from docx.shared import Cm, Mm, Pt, Inches
from os import path
from django.http import FileResponse
from docx2pdf import convert
from io import BytesIO


@permission_required('covid19report.can_access_covid_19_report', login_url='/accounts/login/')
def ViewCovid19Report(request):
	user_language = getDefaultLanguage(request.user.username)
	translation.activate(user_language)	

	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION  
	today_day = timezone.now().strftime('%d')
	today_month = timezone.now().strftime('%m')
	today_year = timezone.now().year
	today_date = str(today_day) + "-" + today_month + "-" + str(today_year)	

	return render(request, 'covid19report/report_by_person.html', {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version,
        'db_server': db_server, 
        'today_date': today_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
	})


@permission_required('covid19report.can_access_covid_19_report', login_url='/accounts/login/')
def AjaxCovid19Report(request):    
	today_date = settings.TODAY_DATE.strftime("%d/%m/%Y")
	emp_id = request.POST.get('emp_id')
	get_vaccine_status_option = request.POST.get('get_vaccine_status_option')

	# print("AJAX Debug : ", emp_id)
	# print("AJAX Debug : ", get_vaccine_status_option)
	employee_obj = None
	record = {}	
	message = ""
	full_name = ""
	phone_number = ""


	sql = "select * from covid_employee_vaccine_update where emp_id=" + str(emp_id) + " and get_vaccine_status=" + str(get_vaccine_status_option) + ";"	
	try:                
		cursor = connection.cursor()
		cursor.execute(sql)
		employee_obj = cursor.fetchone()		
	except db.OperationalError as e:
		message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	except db.Error as e:
		message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	finally:
		cursor.close()

	if employee_obj is not None:
		full_name = employee_obj[1]
		phone_number = employee_obj[2]
		
		get_vaccine_status = employee_obj[3]
		get_vaccine_date = employee_obj[4].strftime("%d/%m/%Y")
		get_vaccine_time = employee_obj[4].strftime("%H:00")
		get_vaccine_place = employee_obj[5]
		file_attach_data = b64encode(employee_obj[7]).decode("utf-8")
		file_attach_type = employee_obj[8]

		if get_vaccine_status_option=="1":
			get_vaccine_status_option_text = "นัดหมายเพื่อฉีดวัคซีนข็มที่ 1"
		elif get_vaccine_status_option=="2":
			get_vaccine_status_option_text = "ได้รับการฉีดวัคซีนเข็มที่ 1 เรียบร้อยแล้ว"
		elif get_vaccine_status_option=="3":
			get_vaccine_status_option_text = "นัดหมายเพื่อฉีดวัคซีนข็มที่ 2"
		elif get_vaccine_status_option=="4":
			get_vaccine_status_option_text = "ได้รับการฉีดวัคซีนเข็มที่ 2 เรียบร้อยแล้ว"

		response = JsonResponse(data={        
			"is_error": False,
			"message": "",
			"emp_id": emp_id,
			"full_name": full_name,
			"phone_number": phone_number,
			"get_vaccine_date": get_vaccine_date,
			"get_vaccine_time": get_vaccine_time,
			"get_vaccine_place": get_vaccine_place,
			"get_vaccine_status_option_text": get_vaccine_status_option_text,
			"file_attach_data": file_attach_data,
			"file_attach_type": file_attach_type,
		})
	else:
		response = JsonResponse(data={        
			"is_error": True,
			"message": "ไม่พบข้อมูล",
			"emp_id": emp_id,
			"full_name": full_name,
			"phone_number": phone_number,
		})

	print("full_name : ", full_name)
	print("phone_number : ", phone_number)

	response.status_code = 200
	return response



@permission_required('covid19report.can_access_covid_19_report', login_url='/accounts/login/')
def ViewCovid19ReportByStatus(request):
	user_language = getDefaultLanguage(request.user.username)
	translation.activate(user_language)	

	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION  
	today_day = timezone.now().strftime('%d')
	today_month = timezone.now().strftime('%m')
	today_year = timezone.now().year
	today_date = str(today_day) + "-" + today_month + "-" + str(today_year)	

	return render(request, 'covid19report/report_by_status.html', {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version,
        'db_server': db_server, 
        'today_date': today_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
	})



@permission_required('covid19report.can_access_covid_19_report', login_url='/accounts/login/')
def AjaxReportByStatus(request):    
	today_date = settings.TODAY_DATE.strftime("%d/%m/%Y")
	get_vaccine_status_option = request.POST.get('get_vaccine_status_option')

	employee_obj = None
	employee_list = []
	record = {}	
	message = ""

	sql = "select * from covid_employee_vaccine_update where get_vaccine_status=" + str(get_vaccine_status_option) + ";"
	try:                
		cursor = connection.cursor()
		cursor.execute(sql)
		employee_obj = cursor.fetchall()		
	except db.OperationalError as e:
		message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	except db.Error as e:
		message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	finally:
		cursor.close()

	if employee_obj is not None:
		for item in employee_obj:
			emp_id = item[0]
			full_name = item[1]
			phone_number = item[2]			
			get_vaccine_status = item[3]
			get_vaccine_date = item[4].strftime("%d/%m/%Y")
			get_vaccine_time = item[4].strftime("%H:00")
			get_vaccine_place = item[5]
			file_attach = item[6]
			file_attach_data = b64encode(item[7]).decode("utf-8")
			file_attach_type = item[8]

			if get_vaccine_status_option=="1":
				get_vaccine_status_option_text = "นัดหมายเพื่อฉีดวัคซีนข็มที่ 1"
			elif get_vaccine_status_option=="2":
				get_vaccine_status_option_text = "ได้รับการฉีดวัคซีนเข็มที่ 1 เรียบร้อยแล้ว"
			elif get_vaccine_status_option=="3":
				get_vaccine_status_option_text = "นัดหมายเพื่อฉีดวัคซีนข็มที่ 2"
			elif get_vaccine_status_option=="4":
				get_vaccine_status_option_text = "ได้รับการฉีดวัคซีนเข็มที่ 2 เรียบร้อยแล้ว"

			record = {
				"emp_id": emp_id,
				"full_name": full_name,
				"phone_number": phone_number,
				"get_vaccine_status_option_text": get_vaccine_status_option_text,
				"get_vaccine_date": get_vaccine_date + " " + get_vaccine_time,
				"get_vaccine_place": get_vaccine_place,
				"file_attach": file_attach
			}

			employee_list.append(record)

		response = JsonResponse(data={        
			"is_error": False,
			"message": "",
			"employee_list": list(employee_list),
		})
	else:
		response = JsonResponse(data={        
			"is_error": True,
			"message": "ไม่พบข้อมูล",
			"employee_list": list(employee_list),
		})

	response.status_code = 200
	return response


@permission_required('covid19report.can_access_covid_19_report', login_url='/accounts/login/')
def download_pdf(request, *args, **kwargs):    
	base_url = MEDIA_ROOT + '/covid19/template/'
	template_name = base_url + 'covid19.docx'
	file_name = request.user.username + "_รายงานการฉีดวัคซีนโควิด-19"
	is_error = True	
	error_message = ""
	emp_id = kwargs['emp_id']
	get_vaccine_status_option = kwargs['get_vaccine_status_option']
	employee_info = None

	full_name = ""
	phone_number = ""
	get_vaccine_status_option_text = ""
	get_vaccine_date = ""
	get_vaccine_place = ""

	sql = "select * from covid_employee_vaccine_update where emp_id=" + emp_id + " and get_vaccine_status=" + get_vaccine_status_option + ";"
	print("SQL : ", sql)
	try:        
		cursor = connection.cursor()
		cursor.execute(sql)
		employee_info = cursor.fetchone()
	except db.OperationalError as e:
		is_error = True
		error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	except db.Error as e:
		is_error = True
		error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	finally:
		cursor.close()

	if employee_info is not None:		
		emp_id = employee_info[0]
		full_name = employee_info[1]
		phone_number = employee_info[2]
		get_vaccine_status_option = employee_info[3]
		get_vaccine_date = employee_info[4]
		get_vaccine_place = employee_info[5]
		file_attach_data = b64encode(employee_info[7]).decode("utf-8")

		if get_vaccine_status_option==1:
			get_vaccine_status_option_text = "นัดหมายเพื่อฉีดวัคซีนข็มที่ 1"
		elif get_vaccine_status_option==2:
			get_vaccine_status_option_text = "ได้รับการฉีดวัคซีนเข็มที่ 1 เรียบร้อยแล้ว"
		elif get_vaccine_status_option==3:
			get_vaccine_status_option_text = "นัดหมายเพื่อฉีดวัคซีนข็มที่ 2"
		elif get_vaccine_status_option==4:
			get_vaccine_status_option_text = "ได้รับการฉีดวัคซีนเข็มที่ 2 เรียบร้อยแล้ว"

		document = DocxTemplate(template_name)
		style = document.styles['Normal']
		font = style.font
		font.name = 'AngsanaUPC'
		font.size = Pt(14)

		context = {
			"emp_id": emp_id,
			"full_name": full_name,
			"phone_number": phone_number,
			"get_vaccine_status_option_text": get_vaccine_status_option_text,
			"get_vaccine_date": get_vaccine_date,
			"get_vaccine_place": get_vaccine_place,
		}

		document.render(context)
		
		binary_img = BytesIO(employee_info[7]) 
		document.add_picture(binary_img)

		document.save(MEDIA_ROOT + '/covid19/download/' + file_name + ".docx")    

		docx_file = path.abspath("media\\covid19\\download\\" + file_name + ".docx")
		pdf_file = path.abspath("media\\covid19\\download\\" + file_name + ".pdf")
		convert(docx_file, pdf_file)

		return FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')
