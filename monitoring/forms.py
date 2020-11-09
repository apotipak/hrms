from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class ScheduleMaintenanceForm(forms.Form):
    cus_id = forms.IntegerField()
    cus_brn = forms.IntegerField()
    cus_vol = forms.IntegerField()

    def __init__(self, *args, **kwargs):    	
        super(ScheduleMaintenanceForm, self).__init__(*args, **kwargs)
        self.fields['cus_id'].widget.attrs = {'class': 'form-control form-control-md', 'placeholder': _('Customer ID')}        
        self.fields['cus_id'].error_messages = {'required': _('Please enter data'), 'max_value': _('Incorrect code')}
        self.fields['cus_brn'].widget.attrs = {'class': 'form-control form-control-md', 'placeholder': _('Customer Branch')}        
        self.fields['cus_brn'].error_messages = {'required': _('Please enter data'), 'max_value': _('Incorrect code')}
        self.fields['cus_vol'].widget.attrs = {'class': 'form-control form-control-md', 'placeholder': _('Customer Volume')}        
        self.fields['cus_vol'].error_messages = {'required': _('Please enter data'), 'max_value': _('Incorrect code')}

        '''
        self.fields['cus_id'].initial = "1324"
        self.fields['cus_brn'].initial = "000"
        self.fields['cus_vol'].initial = "001"
        '''
        self.fields['cus_id'].initial = "1544"
        self.fields['cus_brn'].initial = "000"
        self.fields['cus_vol'].initial = "001"        
        

