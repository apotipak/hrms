from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import generic
from .models import Customer
from .forms import CustomerCreateForm, CustomerUpdateForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone


class CustomerListView(PermissionRequiredMixin, generic.ListView):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE
	template_name = 'customer/customer_list.html'
	permission_required = ('system.view_customer')
	model = Customer
	paginate_by = 100

	def get_context_data(self, **kwargs):
		context = super(CustomerListView, self).get_context_data(**kwargs)
		context.update({
            'page_title': settings.PROJECT_NAME,
            'today_date': settings.TODAY_DATE,
            'project_version': settings.PROJECT_VERSION,
            'db_server': settings.DATABASES['default']['HOST'],
            'project_name': settings.PROJECT_NAME,
        })
	
		return context
	
	def get_queryset(self):
        #return Customer.objects.filter(cus_active__exact=1)
		return Customer.objects.filter(cus_id__in=[2094, 2096, 2097]).order_by('cus_id', '-cus_active')


def save_customer_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            
            if request.user.is_superuser:
                obj.upd_by = 'Superuser'
            else:
                obj.upd_by = request.user.first_name

            if obj.upd_flag == 'A':
                obj.upd_flag = 'E'

            obj.upd_date = timezone.now()
            obj.cus_active = 1
            
            obj.save()
            data['form_is_valid'] = True
            customer_list = Customer.objects.all()
            data['html_customer_list'] = render_to_string('partial_customer_list.html', {
                'customer_list': customer_list
            })
            data['message'] = "ทำรายการสำเร็จ"
        else:
            data['form_is_valid'] = False
            data['message'] = "ไม่สามารถทำรายการได้..!"

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)        
    return JsonResponse(data)

def CustomerCreate(request):
    if request.method == 'POST':
        form = CustomerCreateForm(request.POST)
    else:
        form = CustomerCreateForm()

    return save_customer_form(request, form, 'customer/partial_customer_create.html')

def CustomerUpdate(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=customer)
    else:
        form = CustomerUpdateForm(instance=customer)
    return save_customer_form(request, form, 'customer/partial_customer_update.html')

def CustomerDelete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    data = dict()
    if request.method == 'POST':
        customer.delete()
        data['form_is_valid'] = True
        customer_list = Customer.objects.all()
        data['html_customer_list'] = render_to_string('partial_customer_list.html', {
            'customer_list': customer_list
        })
    else:
        context = {'customer': customer}
        data['html_form'] = render_to_string('customer/partial_customer_delete.html', context, request=request)
    return JsonResponse(data)


@login_required(login_url='/accounts/login/')
def PerformanceInformation(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION	
	today_date = settings.TODAY_DATE

	return render(request, 'customer/performance_information.html', {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})

@login_required(login_url='/accounts/login/')
def CustomerReport(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION	
	today_date = settings.TODAY_DATE

	return render(request, 'customer/customer_report.html', {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})
