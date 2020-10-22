from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from customer.models import CusMain, Customer, CusBill
from contract.models import CusContract, CusService
from .forms import ScheduleMaintenanceForm
from django.http import JsonResponse


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
@permission_required('contract.view_dlyplan', login_url='/accounts/login/')
def ajax_get_customer(request):
    cus_id = request.POST.get('cus_id')
    cus_brn = request.POST.get('cus_brn')
    cus_vol = request.POST.get('cus_vol')

    if cus_id is not None and cus_brn is not None:
        try:
            customer = Customer.objects.filter(cus_id=cus_id, cus_brn=cus_brn).get()
            cus_name_th = customer.cus_name_th
            cus_sht_th = customer.cus_sht_th
            cus_add1_th = customer.cus_add1_th
            cus_add2_th = customer.cus_add2_th
            cus_subdist_th = customer.cus_subdist_th

            cus_name_en = customer.cus_name_en
            cus_sht_en = customer.cus_sht_en
            cus_add1_en = customer.cus_add1_en
            cus_add2_en = customer.cus_add2_en
            cus_subdist_en = customer.cus_subdist_en

            cus_zip = customer.cus_zip

            if customer.cus_district_id is not None:
                cus_district_id = customer.cus_district_id
                cus_district_th = customer.cus_district.dist_th
                cus_district_en = customer.cus_district.dist_en
            else:
                cus_district_id = 0
                cus_district_th = ""
                cus_district_en = ""

            if customer.cus_city_id is not None:
                cus_city_th = customer.cus_city.city_th
                cus_city_en = customer.cus_city.city_en
            else:
                cus_city_id = 0
                cus_city_th = ""
                cus_city_en = ""

            if customer.cus_country_id is not None:
                cus_country_th = customer.cus_country.country_th
                cus_country_en = customer.cus_country.country_en
            else:
                cus_country_id = 0
                cus_country_th = ""
                cus_country_en = ""
            
            cus_tel = customer.cus_tel
            cus_fax = customer.cus_fax
            cus_email = customer.cus_email
            
            if customer.site_contact_id is not None:
                site_contact_id_th = customer.site_contact_id
                site_contact_con_fname_th = customer.site_contact.con_fname_th
                site_contact_con_lname_th = customer.site_contact.con_lname_th
                site_contact_con_position_th = customer.site_contact.con_position_th

                site_contact_id_en = customer.site_contact_id
                site_contact_con_fname_en = customer.site_contact.con_fname_en
                site_contact_con_lname_en = customer.site_contact.con_lname_en
                site_contact_con_position_en = customer.site_contact.con_position_en
            else:
                site_contact_id_th = 0
                site_contact_con_fname_th = ""
                site_contact_con_lname_th = ""
                site_contact_con_position_th = ""

                site_contact_id_en = 0
                site_contact_con_fname_en = ""
                site_contact_con_lname_en = ""
                site_contact_con_position_en = ""


            if customer.cus_zone_id is not None:            
                site_contact_cus_zone_id = customer.cus_zone_id
                site_contact_cus_zone_th = customer.cus_zone.zone_th
                site_contact_cus_zone_en = customer.cus_zone.zone_en
            else:
                site_contact_cus_zone_id = 0
                site_contact_cus_zone_th = ""
                site_contact_cus_zone_en = ""

            response = JsonResponse(data={
                # TH
                "success": True,
                "class": "bg-danger",
                "message": "",
                "is_existed": True,
                "cus_name_th": cus_name_th,
                "cus_sht_th": cus_sht_th,
                "cus_add_th": cus_add1_th + " " + cus_add2_th,
                "cus_subdist_th": cus_subdist_th,
                "cus_zip_th": cus_zip,
                "cus_district_id_th": cus_district_id,
                "cus_district_th": cus_district_th,
                "cus_city_th": cus_city_th,
                "cus_country_th": cus_country_th,
                "site_contact_id_th": site_contact_id_th,
                "site_contact_con_th": str(site_contact_id_th) + " | " + str(site_contact_con_fname_th) + " " + str(site_contact_con_lname_th),
                "site_contact_con_position_th": site_contact_con_position_th,
                
                # EN
                "cus_name_en": cus_name_en,
                "cus_sht_en": cus_sht_en,
                "cus_add_en": cus_add1_en + " " + cus_add2_en,
                "cus_subdist_en": cus_subdist_en,
                "cus_zip_en": cus_zip,
                "cus_district_id_en": cus_district_id,
                "cus_district_en": cus_district_en,
                "cus_city_en": cus_city_en,
                "cus_country_en": cus_country_en,                                                            
                "site_contact_id_en": site_contact_id_en,
                "site_contact_con_en": str(site_contact_id_en) + " | " + str(site_contact_con_fname_en) + " " + str(site_contact_con_lname_en),
                "site_contact_con_position_en": site_contact_con_position_en,                

                "cus_tel": cus_tel,
                "cus_fax": cus_fax,
                "cus_email": cus_email,
                "cus_zone_id": site_contact_cus_zone_id,
                "cus_zone_th": site_contact_cus_zone_th,
                "cus_zone_en": site_contact_cus_zone_en,
            })
            response.status_code = 200
            return response
        except Customer.DoesNotExist:            
            response = JsonResponse(data={
                "success": True,
                "class": "bg-danger",
                "message": "",
                "is_existed": False,
                "cus_name_th": "",
                "cus_sht_th": "",
                "cus_add1_th": "",
                "cus_add2_th": "",
                "cus_subdist_th": "",
                "cus_subdist_en": "",
                "cus_name_en": "",
                "cus_sht_en": "",
                "cus_add1_en": "",
                "cus_add2_en": "",
                "cus_subdist_en": "",
                "cus_zip": "",
                "cus_district": "",
                "site_contact": "",
            })
            response.status_code = 200
            return response            
    else:	
	    response = JsonResponse(data={
	        "success": True,
	        "class": "bg-danger",
	        "message": "",
	        "is_existed": False,
	        "cus_name_th": "",
	        "cus_name_en": "",
	    })
	    return response

