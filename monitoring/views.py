from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import DlyPlan, SchPlan
from customer.models import CusMain, Customer, CusBill
from contract.models import CusContract, CusService
from employee.models import Employee
from .forms import ScheduleMaintenanceForm
from django.http import JsonResponse
import datetime
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ScheduleMaintenance(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE	

	template_name = 'monitoring/schedule_maintenance.html'
	response_data = {}
	modified_records = []

	if request.method == "POST":
		print("POST: ScheduleMaintenance()")
		if form.is_valid():          
			form = ScheduleMaintenanceForm(request.POST, user=request.user)
			response_data['form_is_valid'] = True            
		else:            
			response_data['form_is_valid'] = False
		return JsonResponse(response_data)     
	else:
		print("GET: ScheduleMaintenance()")
		form = ScheduleMaintenanceForm()

	return render(request, template_name, {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date, 'form': form,})


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ajax_get_customer(request):
	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	
	print("cnt_id = " + str(cnt_id))

	# if cus_id is not None and cus_brn is not None:
	if cnt_id is not None:
		try:

			# Contract
			cus_contract = CusContract.objects.filter(cnt_id=cnt_id).get()
			cnt_doc_no = cus_contract.cnt_doc_no
			cnt_active = cus_contract.cnt_active
			cnt_sign_frm = cus_contract.cnt_sign_frm.strftime("%d/%m/%Y")
			cnt_sign_to = cus_contract.cnt_sign_to.strftime("%d/%m/%Y")			
			cnt_eff_frm = cus_contract.cnt_eff_frm.strftime("%d/%m/%Y")
			cnt_eff_to = cus_contract.cnt_eff_to.strftime("%d/%m/%Y")
			cnt_wage_name_th = cus_contract.cnt_wage_id.wage_th
			cnt_wage_name_en = cus_contract.cnt_wage_id.wage_en
			cnt_apr_by_name_en = cus_contract.cnt_apr_by.apr_name_en


			# Contract Services
			try:
				cus_service = CusService.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('-srv_active')				
				print("cus_service is found")
				cus_service_list=[]
				for d in cus_service:
					if d.srv_active:
						record = {
						    "srv_id": d.srv_id,
						    "cnt_id": d.cnt_id_id,
						    "srv_rank": d.srv_rank_id,
						    "srv_shif_id": d.srv_shif_id_id,
						    "srv_shift_name": d.srv_shif_id.shf_desc,
						    "srv_shift_text": d.srv_shif_id.shf_desc,
						    "srv_eff_frm": d.srv_eff_frm.strftime("%d/%m/%Y"),
						    "srv_eff_to": d.srv_eff_to.strftime("%d/%m/%Y"),
						    "srv_qty": d.srv_qty,
						    "srv_rate": d.srv_rate,
						    "srv_cost": d.srv_cost,
						    "srv_cost_rate": d.srv_cost_rate,
						    "srv_mon": d.srv_mon,
						    "srv_tue": d.srv_tue,
						    "srv_wed": d.srv_wed,
						    "srv_thu": d.srv_thu,
						    "srv_fri": d.srv_fri,
						    "srv_sat": d.srv_sat,
						    "srv_sun": d.srv_sun,
						    "srv_pub": d.srv_pub,
						    "srv_rem": d.srv_rem,
						    "srv_active": "Y",
						    "upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
						    "upd_by": d.upd_by,
						}
						cus_service_list.append(record)		
			except CusService.DoesNotExist:
				print("cus_service is not found")
				cus_service_list=[]

			# SCH_PLAN			
			try:
				sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('emp_id')
				print("sch_plan is found")
				sch_plan_list = []
				for d in sch_plan:
					if d.sch_active:
						if d.relief:
							relief = 1
						else:
							relief = 0 

						if d.sch_active:
							sch_active = 1
						else:
							sch_active = 0

						record = {
						    "sch_no": d.sch_no,
						    "emp_id": d.emp_id_id,
						    "emp_fname_th": d.emp_id.emp_fname_th,
						    "emp_lname_th": d.emp_id.emp_lname_th,
						    "sch_rank": d.sch_rank,
						    "sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
						    "sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
						    "sch_shf_mon": d.sch_shf_mon,
						    "sch_shf_tue": d.sch_shf_tue,
						    "sch_shf_wed": d.sch_shf_wed,
						    "sch_shf_thu": d.sch_shf_thu,
						    "sch_shf_fri": d.sch_shf_fri,
						    "sch_shf_sat": d.sch_shf_sat,
						    "sch_shf_sun": d.sch_shf_sun,
						    "sch_active": sch_active,
						    "relief": relief,
						    "upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
						    "upd_by": d.upd_by,
						    "upd_flag": d.upd_flag,
						}
						sch_plan_list.append(record)			    
			except SchPlan.DoesNotExist:
				print("sch_plan is not found")
				sch_plan_list = []

			# CUS_MAIN
			try:
			    cus_main = CusMain.objects.filter(cus_id=cus_id).get()
			    cus_main_cus_name_th = cus_main.cus_name_th
			    cus_main_cus_name_en = cus_main.cus_name_en
			    cus_main_cus_tel = cus_main.cus_tel
			except CusMain.DoesNotExist:
				cus_main_cus_name_th = ""
				cus_main_cus_name_en = ""
				cus_main_cus_tel = ""

			# CUS_SITE
			try:
			    customer = Customer.objects.filter(cus_id=cus_id, cus_brn=cus_brn).get()
			    
			    cus_site_name_th = customer.cus_name_th
			    cus_site_sht_th = customer.cus_sht_th
			    cus_site_add1_th = customer.cus_add1_th
			    cus_site_add2_th = customer.cus_add2_th
			    cus_site_subdist_th = customer.cus_subdist_th
			    cus_site_name_en = customer.cus_name_en
			    cus_site_sht_en = customer.cus_sht_en
			    cus_site_add1_en = customer.cus_add1_en
			    cus_site_add2_en = customer.cus_add2_en
			    cus_site_subdist_en = customer.cus_subdist_en
			    cus_site_zip = customer.cus_zip

			    if customer.cus_district_id is not None:
			        cus_site_district_id = customer.cus_district_id
			        cus_site_district_th = customer.cus_district.dist_th
			        cus_site_district_en = customer.cus_district.dist_en
			    else:
			        cus_site_district_id = 0
			        cus_site_district_th = ""
			        cus_site_district_en = ""

			    if customer.cus_city_id is not None:
			        cus_site_city_th = customer.cus_city.city_th
			        cus_site_city_en = customer.cus_city.city_en
			    else:
			        cus_site_city_id = 0
			        cus_site_city_th = ""
			        cus_site_city_en = ""

			    if customer.cus_country_id is not None:
			        cus_site_country_th = customer.cus_country.country_th
			        cus_site_country_en = customer.cus_country.country_en
			    else:
			        cus_site_country_id = 0
			        cus_site_country_th = ""
			        cus_site_country_en = ""
			    
			    cus_site_tel = customer.cus_tel
			    cus_site_fax = customer.cus_fax
			    cus_site_email = customer.cus_email
			    
			    if customer.site_contact_id is not None:
			        cus_site_contact_id_th = customer.site_contact_id
			        cus_site_contact_con_fname_th = customer.site_contact.con_fname_th
			        cus_site_contact_con_lname_th = customer.site_contact.con_lname_th
			        cus_site_contact_con_position_th = customer.site_contact.con_position_th

			        cus_site_contact_id_en = customer.site_contact_id
			        cus_site_contact_con_fname_en = customer.site_contact.con_fname_en
			        cus_site_contact_con_lname_en = customer.site_contact.con_lname_en
			        cus_site_contact_con_position_en = customer.site_contact.con_position_en
			    else:
			        cus_site_contact_id_th = 0
			        cus_site_contact_con_fname_th = ""
			        cus_site_contact_con_lname_th = ""
			        cus_site_contact_con_position_th = ""

			        cus_site_contact_id_en = 0
			        cus_site_contact_con_fname_en = ""
			        cus_site_contact_con_lname_en = ""
			        cus_site_contact_con_position_en = ""


			    if customer.cus_zone_id is not None:            
			        cus_site_contact_cus_zone_id = customer.cus_zone_id
			        cus_site_contact_cus_zone_th = customer.cus_zone.zone_th
			        cus_site_contact_cus_zone_en = customer.cus_zone.zone_en
			    else:
			        cus_site_contact_cus_zone_id = 0
			        cus_site_contact_cus_zone_th = ""
			        cus_site_contact_cus_zone_en = ""

			    response = JsonResponse(data={
			        # CUS_SITE
			        "success": True,
			        "class": "bg-success",
			        "is_existed": True,

			        "cnt_doc_no": cnt_doc_no,
			        "cnt_active": cnt_active,
			        "cnt_sign_frm": cnt_sign_frm,
			        "cnt_sign_to": cnt_sign_to,			        
			        "cnt_eff_frm": cnt_eff_frm,
			        "cnt_eff_to": cnt_eff_to,
			        "cnt_wage_name_th": cnt_wage_name_th,
			        "cnt_wage_name_en": cnt_wage_name_en,
			        "cnt_apr_by_name_en": cnt_apr_by_name_en,

			        "cus_main_cus_name_th": cus_main_cus_name_th,
			        "cus_main_cus_name_en": cus_main_cus_name_en,
			        "cus_main_cus_tel": cus_main_cus_tel,

			        "cus_site_name_th": cus_site_name_th,
			        "cus_site_sht_th": cus_site_sht_th,
			        "cus_site_add_th": cus_site_add1_th + " " + cus_site_add2_th,
			        "cus_site_subdist_th": cus_site_subdist_th,
			        "cus_site_district_id": cus_site_district_id,
			        "cus_site_district_th": cus_site_district_th,
			        "cus_site_city_th": cus_site_city_th,
			        "cus_site_country_th": cus_site_country_th,
			        "cus_site_contact_id_th": cus_site_contact_id_th,
			        "cus_site_contact_name_th": str(cus_site_contact_con_fname_th) + " " + str(cus_site_contact_con_lname_th),
			        "cus_site_contact_position_th": cus_site_contact_con_position_th,
			        "cus_site_name_en": cus_site_name_en,
			        "cus_site_sht_en": cus_site_sht_en,
			        "cus_site_add_en": cus_site_add1_en + " " + cus_site_add2_en,
			        "cus_site_subdist_en": cus_site_subdist_en,
			        "cus_site_zip": cus_site_zip,
			        "cus_site_district_en": cus_site_district_en,
			        "cus_site_city_en": cus_site_city_en,
			        "cus_site_country_en": cus_site_country_en,                                                            
			        "cus_site_contact_id_en": cus_site_contact_id_en,
			        "cus_site_contact_con_en": str(cus_site_contact_id_en) + " | " + str(cus_site_contact_con_fname_en) + " " + str(cus_site_contact_con_lname_en),
			        "cus_site_contact_con_position_en": cus_site_contact_con_position_en,                
			        "cus_site_tel": cus_site_tel,
			        "cus_site_fax": cus_site_fax,
			        "cus_site_email": cus_site_email,
			        "cus_site_contact_cus_zone_id": cus_site_contact_cus_zone_id,
			        "cus_site_contact_cus_zone_th": cus_site_contact_cus_zone_th,
			        "cus_site_contact_cus_zone_en": cus_site_contact_cus_zone_en,

					"cus_service_list": list(cus_service_list),
					"sch_plan_list": list(sch_plan_list),
			    })
			    response.status_code = 200
			except Customer.DoesNotExist:            
			    response = JsonResponse(data={
			        "success": False,
			        "class": "bg-danger",
			        "is_existed": False,
			    })
			    response.status_code = 200
			    return response			    	
		except CusContract.DoesNotExist:
			print("ajax_get_customer() - Customer Number is not found.")
			response = JsonResponse(data={
			    "success": True,
			    "class": "bg-danger",
			    "is_existed": False,
			})			
	else:
		response = JsonResponse(data={
		    "success": True,
		    "class": "bg-danger",
		    "is_existed": False,
		})

	return response



@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def get_customer_service_list(request):
    print("*************************************")
    print("FUNCTION: get_customer_service_list()")
    print("*************************************")

    cnt_id = request.GET["cnt_id"]

    data = CusService.objects.all().exclude(upd_flag='D').filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('-srv_active')
    
    cus_service_list=[]
    for d in data:
        record = {
            "srv_id": d.srv_id,
            "cnt_id": d.cnt_id_id,
            "srv_rank": d.srv_rank_id,
            "srv_shif_id": d.srv_shif_id_id,
            "srv_shift_text": d.srv_shif_id.shf_desc,
            "srv_eff_frm": d.srv_eff_frm.strftime("%d/%m/%Y"),
            "srv_eff_to": d.srv_eff_to.strftime("%d/%m/%Y"),
            "srv_qty": d.srv_qty,
            "srv_rate": d.srv_rate,
            "srv_cost": d.srv_cost,
            "srv_cost_rate": d.srv_cost_rate,
            "srv_mon": d.srv_mon,
            "srv_tue": d.srv_tue,
            "srv_wed": d.srv_wed,
            "srv_thu": d.srv_thu,
            "srv_fri": d.srv_fri,
            "srv_sat": d.srv_sat,
            "srv_sun": d.srv_sun,
            "srv_pub": d.srv_pub,
            "srv_rem": d.srv_rem,
            "srv_active": d.srv_active,
            "upd_date": d.upd_date,
            "upd_by": d.upd_by,
        }
        cus_service_list.append(record)

    response = JsonResponse(data={
        "success": True,
        "cus_service_list": list(cus_service_list),
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ajax_get_customer_schedule_plan_list(request):
    print("*************************************")
    print("FUNCTION: ajax_get_customer_schedule_plan_list()")
    print("*************************************")

    cus_id = request.POST.get('cus_id')
    cus_brn = request.POST.get('cus_brn')
    cus_vol = request.POST.get('cus_vol')
    sch_active = request.POST.get("sch_active")	
    cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
    print("cnt_id = " + str(cnt_id))
    print("sch_active = " + str(sch_active))

    try:    	
    	print("sch_plan is found")
    	sch_plan_list = []
    	total = 0

    	if sch_active == '1':
    		sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('emp_id')
	    	for d in sch_plan:    		
	    		if d.sch_active:
	    			if d.relief:
	    				relief = 1
	    			else:
	    				relief = 0 

	    			if d.sch_active:
	    				sch_active = 1
	    			else:
	    				sch_active = 0


	    			record = {
	    				"sch_no": d.sch_no,
	    				"emp_id": d.emp_id_id,
					    "emp_fname_th": d.emp_id.emp_fname_th,
					    "emp_lname_th": d.emp_id.emp_lname_th,	    				
	    				"sch_rank": d.sch_rank,
	    				"sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
	    				"sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
	    				"sch_shf_mon": d.sch_shf_mon,
	    				"sch_shf_tue": d.sch_shf_tue,
	    				"sch_shf_wed": d.sch_shf_wed,
	    				"sch_shf_thu": d.sch_shf_thu,
	    				"sch_shf_fri": d.sch_shf_fri,
	    				"sch_shf_sat": d.sch_shf_sat,
	    				"sch_shf_sun": d.sch_shf_sun,
	    				"sch_active": sch_active,
	    				"relief": relief,
	    				"upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
	    				"upd_by": d.upd_by,
	    				"upd_flag": d.upd_flag,
	    			}
	    			sch_plan_list.append(record)
    	elif sch_active == '2':
    		sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('emp_id')
	    	for d in sch_plan:    		
	    		if d.sch_active == 0:
	    			if d.relief:
	    				relief = 1
	    			else:
	    				relief = 0 

	    			if d.sch_active:
	    				sch_active = 1
	    			else:
	    				sch_active = 0

	    			record = {
	    				"sch_no": d.sch_no,
	    				"emp_id": d.emp_id_id,
					    "emp_fname_th": d.emp_id.emp_fname_th,
					    "emp_lname_th": d.emp_id.emp_lname_th,	    				
	    				"sch_rank": d.sch_rank,
	    				"sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
	    				"sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
	    				"sch_shf_mon": d.sch_shf_mon,
	    				"sch_shf_tue": d.sch_shf_tue,
	    				"sch_shf_wed": d.sch_shf_wed,
	    				"sch_shf_thu": d.sch_shf_thu,
	    				"sch_shf_fri": d.sch_shf_fri,
	    				"sch_shf_sat": d.sch_shf_sat,
	    				"sch_shf_sun": d.sch_shf_sun,
	    				"sch_active": sch_active,
	    				"relief": relief,
	    				"upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
	    				"upd_by": d.upd_by,
	    				"upd_flag": d.upd_flag,
	    			}
	    			sch_plan_list.append(record)
    	elif sch_active == '3':
    		sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('-sch_active', 'emp_id')
	    	for d in sch_plan:
    			if d.relief:
    				relief = 1
    			else:
    				relief = 0 

    			if d.sch_active:
    				sch_active = 1
    			else:
    				sch_active = 0

    			record = {
    				"sch_no": d.sch_no,
    				"emp_id": d.emp_id_id,
				    "emp_fname_th": d.emp_id.emp_fname_th,
				    "emp_lname_th": d.emp_id.emp_lname_th,    				
    				"sch_rank": d.sch_rank,
    				"sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
    				"sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
    				"sch_shf_mon": d.sch_shf_mon,
    				"sch_shf_tue": d.sch_shf_tue,
    				"sch_shf_wed": d.sch_shf_wed,
    				"sch_shf_thu": d.sch_shf_thu,
    				"sch_shf_fri": d.sch_shf_fri,
    				"sch_shf_sat": d.sch_shf_sat,
    				"sch_shf_sun": d.sch_shf_sun,
    				"sch_active": sch_active,
    				"relief": relief,
    				"upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
    				"upd_by": d.upd_by,
    				"upd_flag": d.upd_flag,
    			}
    			sch_plan_list.append(record)	    	
    	else:
	    	print("sch_plan is not found")    	
	    	sch_plan_list = []

    except SchPlan.DoesNotExist:
    	print("sch_plan is not found")    	
    	sch_plan_list = []

    response = JsonResponse(data={
        "success": True,
        "sch_plan_list": list(sch_plan_list),
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ajax_get_customer_schedule_plan(request):
    print("*************************************")
    print("FUNCTION: ajax_get_customer_schedule_plan()")
    print("*************************************")

    cus_id = request.POST.get('cus_id')
    cus_brn = request.POST.get('cus_brn')
    cus_vol = request.POST.get('cus_vol')
    sch_no = request.POST.get("sch_no")	
    cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
    print("sch_no = " + str(sch_no))

    try:
    	sch_plan = SchPlan.objects.filter(sch_no=sch_no).get()

    	print("debug : " + str(sch_plan.emp_id_id) + str(sch_plan.sch_rank))
    	print("sch_active = " + str(sch_plan.sch_active))


    	if sch_plan.relief:
    		relief = 1
    	else:
    		relief = 0 
    	if sch_plan.sch_active:
    		sch_active = 1
    	else:
    		sch_active = 0

    	if sch_plan.emp_id.emp_term_date is not None:
    		emp_term_date = sch_plan.emp_id.emp_term_date.strftime("%d/%m/%Y"),
    	else:
    		emp_term_date = ""

    	if int(sch_plan.sch_shf_sat) == 99:
    		# sch_shf_sat = "DAY OFF"
    		sch_shf_sat = sch_plan.sch_shf_sat 
    	else:
    		sch_shf_sat = sch_plan.sch_shf_sat 


    	if int(sch_plan.sch_shf_sun) == 99:
    		# sch_shf_sun = "DAY OFF"
    		sch_shf_sun = sch_plan.sch_shf_sun 
    	else:
    		sch_shf_sun = sch_plan.sch_shf_sun 

    	response = JsonResponse(data={
	        "success": True,
			"sch_no": sch_plan.sch_no,
			"emp_id": sch_plan.emp_id_id,
		    "emp_fname_th": sch_plan.emp_id.emp_fname_th,
		    "emp_lname_th": sch_plan.emp_id.emp_lname_th,
		    "emp_status_id": sch_plan.emp_id.emp_status_id,
		    "emp_status": sch_plan.emp_id.emp_status.sts_th,
		    "emp_type": sch_plan.emp_id.emp_type,
			"sch_rank": sch_plan.sch_rank,
			"emp_join_date": sch_plan.emp_id.emp_join_date.strftime("%d/%m/%Y"),
			"emp_term_date": emp_term_date,
			"sch_date_frm": sch_plan.sch_date_frm.strftime("%d/%m/%Y"),
			"sch_date_to": sch_plan.sch_date_to.strftime("%d/%m/%Y"),
			"sch_shf_mon": sch_plan.sch_shf_mon,
			"sch_shf_tue": sch_plan.sch_shf_tue,
			"sch_shf_wed": sch_plan.sch_shf_wed,
			"sch_shf_thu": sch_plan.sch_shf_thu,
			"sch_shf_fri": sch_plan.sch_shf_fri,
			"sch_shf_sat": sch_shf_sat,
			"sch_shf_sun": sch_shf_sun,
			"sch_active": sch_active,
			"relief": relief,
			"upd_date": sch_plan.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
			"upd_by": sch_plan.upd_by,
			"upd_flag": sch_plan.upd_flag,	        
   		})					    		   
    except SchPlan.DoesNotExist:
	    response = JsonResponse(data={
	        "success": True,
	        "sch_plan": list(record),
	    })

    response.status_code = 200
    return response



@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ajax_save_customer_schedule_plan(request):
	print("*************************************")
	print("FUNCTION: ajax_save_customer_schedule_plan()")
	print("*************************************")

	selected_sch_no = request.POST.get("selected_sch_no")
	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')    
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	emp_id = request.POST.get("selected_sch_no")	
	sch_active = request.POST.get("sch_active")
	relief = request.POST.get("relief")
	mon_shift = request.POST.get("mon_shift")
	tue_shift = request.POST.get("tue_shift")
	wed_shift = request.POST.get("wed_shift")
	thu_shift = request.POST.get("thu_shift")
	fri_shift = request.POST.get("fri_shift")
	sat_shift = request.POST.get("sat_shift")
	sun_shift = request.POST.get("sun_shift")
	
	sch_plan_list = []

	print("relief = " + str(relief))
	print("sat_shift = " + str(sat_shift))
	print("sun_shift = " + str(sun_shift))
	print("sch_active = " + str(sch_active))

	if len(selected_sch_no) > 0:
		try:
			sch_plan = SchPlan.objects.filter(sch_no=selected_sch_no).get()
			sch_plan.sch_active = sch_active
			sch_plan.relief = relief
			sch_plan.sch_shf_mon = mon_shift
			sch_plan.sch_shf_tue = tue_shift
			sch_plan.sch_shf_wed = wed_shift
			sch_plan.sch_shf_thu = thu_shift
			sch_plan.sch_shf_fri = fri_shift
			sch_plan.sch_shf_sat = sat_shift
			sch_plan.sch_shf_sun = sun_shift
			sch_plan.sch_upd_date = datetime.datetime.now()
			sch_plan.upd_by = request.user.first_name
			sch_plan.upd_flag = 'E'			
			sch_plan.save()

			# generate new security guard list		
			sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('emp_id')			
			for d in sch_plan:
				if d.sch_active:
					if d.relief:
						relief = 1
					else:
						relief = 0 

					if d.sch_active:
						sch_active = 1
					else:
						sch_active = 0

					record = {
					    "sch_no": d.sch_no,
					    "emp_id": d.emp_id_id,
					    "emp_fname_th": d.emp_id.emp_fname_th,
					    "emp_lname_th": d.emp_id.emp_lname_th,
					    "sch_rank": d.sch_rank,
					    "sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
					    "sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
					    "sch_shf_mon": d.sch_shf_mon,
					    "sch_shf_tue": d.sch_shf_tue,
					    "sch_shf_wed": d.sch_shf_wed,
					    "sch_shf_thu": d.sch_shf_thu,
					    "sch_shf_fri": d.sch_shf_fri,
					    "sch_shf_sat": d.sch_shf_sat,
					    "sch_shf_sun": d.sch_shf_sun,
					    "sch_active": sch_active,
					    "relief": relief,
					    "upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
					    "upd_by": d.upd_by,
					    "upd_flag": d.upd_flag,
					}
					sch_plan_list.append(record)

			response = JsonResponse(data={
				"message": "Saved success.",
				"class": "bg-success",
				"sch_plan_list": list(sch_plan_list),
			})
		except SchPlan.DoesNotExist:
			response = JsonResponse(data={
				"message": "Schedule Number is not found.",
				"class": "bg-danger",
				"sch_plan_list": list(sch_plan_list),
			})
	else:
		response = JsonResponse(data={
			"message": "No data",
			"class": "bg-danger",
			"sch_plan_list": list(sch_plan_list),
		})
    
	response.status_code = 200
	return response
    


#@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_get_employee_list(request):

	print("***********************************")
	print("FUNCTION: ajax_get_employee_list()")
	print("***********************************")

	emp_id = request.GET.get('emp_id')
	print("debug: emp_id = " + str(emp_id))

	item_per_page = 50

	if emp_id is not None:
	    if emp_id != "":
	        if emp_id.isnumeric():
	            print("debug1")
	            data = Employee.objects.filter(emp_id__exact=emp_id).filter(emp_type='D1').get()
	        else:
	            print("debug3")
	            data = Employee.objects.all().filter(emp_type='D1')[:10]
	    else:
	        print("debug4")
	        data = Employee.objects.filter(emp_type='D1').filter(empstatus='A').exclude(upd_flag='D').order_by('emp_id')[:10]
	else:		
	    print("debug5")
	    data = Employee.objects.all().filter(emp_type='D1')[:10]

	for d in data:
		print("emp_id = " + str(d.emp_id))


	paginator = Paginator(data, item_per_page)
	is_paginated = True if paginator.num_pages > 1 else False
	page = request.GET.get('page', 1) or 1

	try:
	    current_page = paginator.get_page(page)
	except InvalidPage as e:
	    raise Http404(str(e))    

	# amnaj
	if current_page:
		try:
			print("debug 1")
			current_page = paginator.get_page(page)
		except InvalidPage as e:
			print("debug 2")
			raise Http404(str(e))

		if current_page:
		    current_page_number = current_page.number
		    current_page_paginator_num_pages = current_page.paginator.num_pages

		    pickup_dict = {}
		    pickup_records=[]

		    for d in current_page:
		    	emp_id = d.emp_id
		    	emp_fname_th = d.emp_fname_th
		    	emp_lname_th = d.emp_lname_th
		    	emp_fname_en = d.emp_fname_en
		    	emp_lname_en = d.emp_lname_en

		    	record = {
		    		"emp_id": emp_id,
		    		"emp_fname_th": emp_fname_th,
		    		"emp_lname_th": emp_lname_th,
		    		"emp_fname_en": emp_fname_en,
		    		"emp_lname_en": emp_lname_en,		    		
		    	}
		    	pickup_records.append(record)

		    response = JsonResponse(data={
		    	"success": True,
		        "is_paginated": is_paginated,
		        "page" : page,
		        #"next_page" : page + 1,
		        "current_page_number" : current_page_number,
		        "current_page_paginator_num_pages" : current_page_paginator_num_pages,
		        "results": list(pickup_records)         
		        })
		    response.status_code = 200
		    return response
		else:
			print("debug 3")
			print("error 403")
			response = JsonResponse({"error": "there was an error"})
			response.status_code = 403
			return response
	else:
		print("debug 4")
		response = JsonResponse({"error": "there was an error"})
		response.status_code = 403
		return response

	return JsonResponse(data={"success": False, "results": ""})