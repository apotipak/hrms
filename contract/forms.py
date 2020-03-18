from django import forms
from .models import CusContract
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ContractForm(forms.ModelForm):
    customer_id = forms.IntegerField(label='Customer ID', required=True)
    customer_branch = forms.IntegerField(label='Branch', required=True)
    customer_volume = forms.IntegerField(label='Volume', required=True)

    class Meta:
        model = CusContract
        fields = ['cus_id', 'cus_brn', 'cus_vol']
        error_messages = {
            'customer_id': {
                'required': _("This field is required"),
            }
        }

    def __init__(self, *args, **kwargs):    	
        super(ContractForm, self).__init__(*args, **kwargs)        
        self.fields['customer_id'].widget.attrs={'class': 'form-control', 'placeholder': _('Customer ID')}
        self.fields['customer_branch'].widget.attrs={'class': 'form-control', 'placeholder': _('Branch')}
        self.fields['customer_branch'].widget.attrs['max'] = 3
        self.fields['customer_volume'].widget.attrs={'class': 'form-control', 'placeholder': _('Volume')}

    def clean_customer_id(self):
        if self.instance: 
            return self.instance.cus_id
        else: 
            return self.fields['cus_id']

    def clean_customer_branch(self):
        if self.instance: 
            return self.instance.cus_brn
        else: 
            return self.fields['cus_brn']

    def clean_customer_volume(self):
        if self.instance: 
            return self.instance.cus_vol
        else: 
            return self.fields['cus_vol']

    
