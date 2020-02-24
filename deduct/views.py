from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url='/accounts/login/')
def DeductList(request):
	page_title = settings.PROJECT_NAME
	return render(request, 'deduct/deduct_list.html', {'page_title': page_title})
