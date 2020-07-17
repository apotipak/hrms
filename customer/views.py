from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import generic
from .models import Customer
from .forms import CustomerCreateForm, CustomerUpdateForm
from .forms import CustomerSearchForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@permission_required('customer.view_customer', login_url='/accounts/login/')
def CustomerList(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = settings.TODAY_DATE    
    item_per_page = 30    

    if request.method == "POST":
        print("post")
        form = CustomerSearchForm(request.POST, user=request.user)
        cus_id = request.POST.get('cus_id')
        cus_brn = request.POST.get('cus_brn')
        if cus_id != '' and cus_brn != '':
            print("test1")
            customer_list = Customer.objects.filter(cus_id=cus_id,cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        if cus_id == '' and cus_brn == '':
            print("test2")
            customer_list = Customer.objects.all().order_by('cus_id','cus_brn','-cus_active')
        
        if cus_id == '' and cus_brn != '':
            print("test3")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        if cus_id != '' and cus_brn == '':
            print("test4")
            customer_list = Customer.objects.filter(cus_id=cus_id).order_by('-cus_active','cus_id','cus_brn')

        print("POST: cus_id = " +  str(cus_id))
        print("POST: cus_brn = " +  str(cus_brn))
        
        page = 1
        paginator = Paginator(customer_list, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))        
    else:
        form = CustomerSearchForm(user=request.user)                    
        cus_id = request.GET.get('cusid', '')
        cus_brn = request.GET.get('brn', '')

        if cus_id != '' and cus_brn != '':
            customer_list = Customer.objects.filter(cus_id=cus_id,cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        if cus_id == '' and cus_brn == '':
            customer_list = Customer.objects.all().order_by('-cus_active','cus_id','cus_brn')
        
        if cus_id == '' and cus_brn != '':
            customer_list = Customer.objects.filter(cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        if cus_id != '' and cus_brn == '':
            customer_list = Customer.objects.filter(cus_id=cus_id).order_by('-cus_active','cus_id','cus_brn')

        paginator = Paginator(customer_list, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page', '1') or 1

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))

        # customer_list = []
    
    context = {
        'page_title': page_title, 
        'db_server': db_server, 'today_date': today_date,
        'project_name': project_name, 
        'project_version': project_version,         
        'current_page': current_page,
        'is_paginated': is_paginated,
        'customer_list': customer_list,
        'form': form,
        'cus_id': cus_id,
        'cus_brn': cus_brn,
    }

    return render(request, 'customer/customer_list.html', context)

class CustomerListView1(PermissionRequiredMixin, generic.ListView):
    permission_required = ('customer.view_customer')    
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = settings.TODAY_DATE
        
    model = Customer
    template_name = 'customer/customer_list.html'
    context_object_name = 'customer_list'
    paginate_by = 5

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
        return Customer.objects.filter(cus_active__exact=1)


def save_customer_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        #form = CustomerCreateForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            fields = request.POST.dict()

            if request.user.is_superuser:
                obj.upd_by = 'Superuser'
            else:
                obj.upd_by = request.user.first_name

            if obj.upd_flag == 'A':
                obj.upd_flag = 'E'

            # Check duplicate Customer No
            cus_no = fields.get('cus_id') + fields.get('cus_brn').zfill(3)            
            obj.cus_no = cus_no

            # Get current date time
            obj.upd_date = timezone.now()
            obj.cus_active = 1
            
            obj.save()

            data['form_is_valid'] = True
            
            # TODO:
            #customer_list = Customer.objects.all()
            customer_list = Customer.objects.filter(cus_id__in=[2094]).order_by('-upd_date', 'cus_id', '-cus_active')

            data['html_customer_list'] = render_to_string('customer/partial_customer_list.html', {
                'customer_list': customer_list
            })
            data['message'] = "ทำรายการสำเร็จ"
        else:
            data['form_is_valid'] = False
            #data['message'] = "ไม่สามารถทำรายการได้!! กรุณาตรวจสอบข้อมูล"
            
            for field in form.errors:
                if field == 'cus_no':
                    print(field)
                    data['message'] = "รหัสสาขานี้มีอยู่แล้ว"                
                else:
                    data['message'] = "กรุณาป้อนข้อมูลให้ครบถ้วน"
            
            #print(form.errors)

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)        
    return JsonResponse(data)

"""
def CustomerCreate(request):
    if request.method == 'POST':
        form = CustomerCreateForm(request.POST)
    else:
        form = CustomerCreateForm()

    return save_customer_form(request, form, 'customer/partial_customer_create.html')
"""

@login_required(login_url='/accounts/login/')
def CustomerCreate(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    today_date = settings.TODAY_DATE

    return render(request, 'customer/customer_create.html', {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})

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
        #customer_list = Customer.objects.all()
        customer_list = Customer.objects.filter(cus_id__in=[2094]).order_by('-upd_date', 'cus_id', '-cus_active')
        data['html_customer_list'] = render_to_string('customer/partial_customer_list.html', {
            'customer_list': customer_list
        })
        data['message'] = "ทำรายการสำเร็จ"
    else:
        data['message'] = "ไม่สามารถทำรายการได้..!"
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
