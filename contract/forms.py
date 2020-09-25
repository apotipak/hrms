from django import forms
from .models import CusContract
from customer.models import Customer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ContractForm(forms.ModelForm):
    print("debug ContractForm")
    cus_id = forms.DecimalField(label='Customer ID', required=False, max_value=9999999)
    cus_brn = forms.DecimalField(label='Branch', required=False, max_value=999, min_value=0)
    cus_vol = forms.DecimalField(label='Volume', required=False, max_value=999, min_value=0)

    class Meta:
        model = CusContract
        fields = ['cus_brn', 'cus_vol', 'cus_id'] 

    def __init__(self, *args, **kwargs):    	
        super(ContractForm, self).__init__(*args, **kwargs)

        self.fields['cus_id'].widget.attrs = {'class': 'form-control form-control-sm', 'placeholder': _('Customer ID')}        
        self.fields['cus_id'].error_messages = {'required': _('กรุณาป้อนข้อมูล'), 'max_value': _('รหัสสัญญาเกิน 7 หลัก')}

        self.fields['cus_brn'].widget.attrs={'class': 'form-control form-control-sm', 'placeholder': _('Branch')}
        self.fields['cus_brn']._messages = {'required': _('กรุณาป้อนข้อมูล'), 'max_value': _('รหัสสาขาเกิน 3 หลัก'), 'min_value': _('ป้อนข้อมูลน้อยกว่า 0')}

        self.fields['cus_vol'].widget.attrs={'class': 'form-control form-control-sm', 'placeholder': _('Volume')}
        self.fields['cus_vol'].error_messages = {'required': _('กรุณาป้อนข้อมูล'), 'max_value': _('รหัสลำดับสัญญาเกิน 3 หลัก'), 'min_value': _('ป้อนข้อมูลน้อยกว่า 0')}

    def clean_cus_id(self):
        if self.instance: 
            return self.instance.cus_id
        else: 
            return self.fields['cus_id']
        
    def clean_cus_brn(self):
        if self.instance: 
            return self.instance.cus_brn
        else: 
            return self.fields['cus_brn']

    def clean_cus_vol(self):
        if self.instance: 
            return self.instance.cus_vol
        else: 
            return self.fields['cus_vol']


class ContractUpdateForm(forms.ModelForm):
    # cnt_id = forms.CharField(required=False)
    cnt_active = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput())
    cnt_doc_no = forms.CharField(required=False)    
    # cnt_wage_id = forms.CharField(required=False) 
    # cnt_apr_by = forms.CharField(required=False)

    print("debug ContractUpdateForm")

    class Meta:
        model = CusContract        
        fields = '__all__'
        exclude = ['cnt_id'],

    def __init__(self, *args, **kwargs):
        super(ContractUpdateForm, self).__init__(*args, **kwargs)        
        instance = getattr(self, 'instance', None)

        # self.fields['cnt_doc_no'].error_messages = {'required': _('กรุณาป้อนข้อมูล'), 'max_value': _('รหัสสัญญาเกิน 7 หลัก')}
        # self.fields['cnt_doc_no'].error_messages = {'required': _('Contract Ref. is required.')}

    '''
    def clean_cnt_id(self):
        data = self.data.get('cnt_id')        
        return data
    '''
    def clean(self):
        data = self.cleaned_data
        return data

    '''
    def clean_cnt_wage_id(self):
        data = self.data.get('cnt_wage_id')
        return data

    def clean_cnt_apr_by(self):
        data = self.data.get('cnt_apr_by')
        return data
    '''

