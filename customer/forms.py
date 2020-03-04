from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput


class CustomerCreateForm(forms.ModelForm):    
    class Meta:
        model = Customer
        fields = ('cus_no', 'cus_id', 'cus_name_th')
        widgets = {
            #'upd_by': forms.HiddenInput(),
            #'upd_flag': forms.HiddenInput()
        }
        error_messages = {
            'cus_no': {
                'required': "This field is required",
            }
        }

    def __init__(self, *args, **kwargs):
        super(CustomerCreateForm, self).__init__(*args, **kwargs)
        self.fields['cus_no'].label = "Customer Number"
        self.fields['cus_id'].label = "Customer ID"
        #self.fields['apr_name_th'].label = "Name (TH)"
        #self.fields['apr_pos_th'].label = "Position (TH)"
        #self.fields['apr_piority'].label = "Priority Type"
        #self.initial['upd_flag'] = 'A'
        #self.initial['upd_by'] = 'Superadmin'

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('cus_no', 'cus_id', 'cus_name_th')

    def __init__(self, *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['cus_no'].widget.attrs['readonly'] = True
        self.fields['cus_no'].label = "Customer Number"
        self.fields['cus_id'].widget.attrs['readonly'] = True
        self.fields['cus_id'].label = "Customer ID"
        self.fields['cus_name_th'].label = "Customer Name (TH)"
        
    def clean_cus_no(self):
        if self.instance: 
            return self.instance.cus_no
        else: 
            return self.fields['cus_no']
