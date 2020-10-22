from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from contract.models import CusContract, CusService
from .forms import ScheduleMaintenanceForm


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_monitoring', login_url='/accounts/login/')
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
