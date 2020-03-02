from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import generic
from system.models import TAprove
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import CompanyApprovePriorityForm


@login_required(login_url='/accounts/login/')
def Index(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE		

	return render(request, 'system/index.html', {
        'page_title': page_title,
        'project_name': project_name,
        'project_version': project_version,
        'db_server': db_server,
        'today_date': today_date
    })	


class CompanyApprovePriorityListView(PermissionRequiredMixin, generic.ListView):
    template_name = 'system/company_approve_priority_list.html'    
    permission_required = ('system.view_taprove')
    model = TAprove
    #paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(CompanyApprovePriorityListView, self).get_context_data(**kwargs)
        context.update({
            'page_title': settings.PROJECT_NAME,
            'today_date': settings.TODAY_DATE,
            'project_version': settings.PROJECT_VERSION,
            'db_server': settings.DATABASES['default']['HOST'],
            'project_name': settings.PROJECT_NAME,
        })

        return context

    def get_queryset(self):
        return TAprove.objects.all()


class CompanyApprovePriorityDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = ('system.view_taprove')
    model = TAprove


def save_company_approve_priority_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            taprove_list = TAprove.objects.all()
            data['html_company_approve_priority_list'] = render_to_string('system/company/partial_approve_priority_list.html', {
                'taprove_list': taprove_list
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def CompanyApprovePriorityDelete(request, pk):
    company_approve_priority = get_object_or_404(TAprove, pk=pk)
    data = dict()
    if request.method == 'POST':
        company_approve_priority.delete()
        data['form_is_valid'] = True
        taprove_list = TAprove.objects.all()
        data['html_company_approve_priority_list'] = render_to_string('system/company/partial_approve_priority_list.html', {
            'taprove_list': taprove_list
        })
    else:
        context = {'company_approve_priority': company_approve_priority}
        data['html_form'] = render_to_string('system/company/partial_approve_priority_delete.html', context, request=request)
    return JsonResponse(data)


def CompanyApprovePriorityCreate(request):
    if request.method == 'POST':
        form = CompanyApprovePriorityForm(request.POST)
    else:
        form = CompanyApprovePriorityForm()
    return save_company_approve_priority_form(request, form, 'system/company/partial_approve_priority_create.html')


@login_required(login_url='/accounts/login/')
def CompanyInformation(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE

	return render(request, 'system/company_information.html', {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})
