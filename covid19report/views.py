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
from base64 import b64encode


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
	print("SQL : ", sql)
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


	if employee_obj is not None:
		full_name = employee_obj[1]
		phone_number = employee_obj[2]
		
		get_vaccine_status = employee_obj[3]
		get_vaccine_date = employee_obj[4].strftime("%d/%m/%Y")
		get_vaccine_time = employee_obj[4].strftime("%H:%M")
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

