from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url='/accounts/login/')
def IncomeDeductList(request):
	page_title = settings.PROJECT_NAME
	return render(request, 'income/income_deduct_list.html', {'page_title': page_title})
