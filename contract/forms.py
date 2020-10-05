from django import forms
from .models import CusContract
from customer.models import Customer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


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

        # self.fields['cus_vol'].widget.attrs={'class': 'form-control form-control-sm', 'placeholder': _('Volume')}
        # self.fields['cus_vol'].error_messages = {'required': _('กรุณาป้อนข้อมูล'), 'max_value': _('รหัสลำดับสัญญาเกิน 3 หลัก'), 'min_value': _('ป้อนข้อมูลน้อยกว่า 0')}

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
    cnt_active = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    cnt_doc_no = forms.CharField(required=False)
    cnt_apr_by_id = forms.CharField(required=False)
    cnt_doc_date = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))
    cnt_eff_frm = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))
    cnt_eff_to = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))
    cnt_sign_frm = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))
    cnt_sign_to = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))

    class Meta:
        model = CusContract  
        fields = '__all__'
        exclude = ['cnt_id', 'cus_brn', 'cus_vol']

    def __init__(self, *args, **kwargs):
        super(ContractUpdateForm, self).__init__(*args, **kwargs)        
        instance = getattr(self, 'instance', None)        
        self.fields['cnt_doc_no'].error_messages = {'required': _('<b>Contract Ref.</b> is required.')}
        self.fields['cnt_doc_date'].error_messages = {'required': _('<b>Contract Date</b> is required.')}
                
        self.fields['cnt_doc_date'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_doc_date', 'placeholder': _('')})
        self.fields['cnt_eff_frm'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_eff_frm', 'placeholder': _('dd/mm/yyyy')})
        self.fields['cnt_eff_to'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_eff_to', 'placeholder': _('dd/mm/yyyy')})
        self.fields['cnt_sign_frm'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_sign_frm', 'placeholder': _('dd/mm/yyyy')})
        self.fields['cnt_sign_to'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_sign_to', 'placeholder': _('dd/mm/yyyy')})
        
    def clean_cnt_doc_no(self):
        data = self.data.get('cnt_doc_no')
        if len(data) == '0':
            raise ValidationError("Contrct Ref. is required.")
        return data


class ContractCreateForm(forms.ModelForm):
    cnt_id = forms.DecimalField(label='Contract ID', required=False)
    cus_id = forms.DecimalField(label='Customer ID', required=False)
    cus_brn = forms.DecimalField(label='Customer Branch', required=False)
    cus_vol = forms.DecimalField(label='Customer Volume', required=False)
    cnt_apr_by_text = forms.CharField(required=False)

    # Date format
    cnt_doc_date = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))
    cnt_eff_frm = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))
    cnt_eff_to = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))
    cnt_sign_frm = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))
    cnt_sign_to = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y', ))

    cnt_guard_amt = forms.DecimalField(required=False, min_value=0)
    cnt_sale_amt = forms.DecimalField(required=False, min_value=0)

    class Meta:
        model = CusContract  
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContractCreateForm, self).__init__(*args, **kwargs)        
        instance = getattr(self, 'instance', None)                        
        self.fields['cus_id'].widget.attrs.update({'class': 'form-control form-control-sm col-3', 'placeholder': _('')})
        self.fields['cus_brn'].widget.attrs.update({'class': 'form-control form-control-sm col-2', 'placeholder': _('')})
        self.fields['cus_vol'].widget.attrs.update({'class': 'form-control form-control-sm col-2', 'placeholder': _('')})

        self.fields['cnt_doc_date'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_doc_date', 'placeholder': _('dd/mm/yyyy')})
        self.fields['cnt_eff_frm'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_eff_frm', 'placeholder': _('dd/mm/yyyy')})
        self.fields['cnt_eff_to'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_eff_to', 'placeholder': _('dd/mm/yyyy')})
        self.fields['cnt_sign_frm'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_sign_frm', 'placeholder': _('dd/mm/yyyy')})
        self.fields['cnt_sign_to'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_sign_to', 'placeholder': _('dd/mm/yyyy')})
        self.fields['cnt_apr_by_text'].widget.attrs.update({'class': 'form-control form-control-sm', 'id': 'id_cnt_apr_by_text'})
        self.fields['cnt_guard_amt'].widget.attrs.update({'class': 'form-control form-control-sm text-right', 'id': 'id_cnt_guard_amt'})
        self.fields['cnt_sale_amt'].widget.attrs.update({'class': 'form-control form-control-sm text-right', 'id': 'id_cnt_sale_amt'})
        self.fields['cnt_guard_amt'].widget.attrs['readonly'] = True
        self.fields['cnt_sale_amt'].widget.attrs['readonly'] = True

        # Initial value
        self.fields['cnt_doc_date'].initial = datetime.date.today
        self.fields['cnt_eff_frm'].initial = datetime.date.today
        self.fields['cnt_eff_to'].initial = datetime.date.today
        self.fields['cnt_sign_frm'].initial = datetime.date.today
        self.fields['cnt_sign_to'].initial = datetime.date.today
        self.fields['cnt_apr_by_text'].initial = "ดร.ชนัต สุขสุวรรณธร (Dr.Chanat Suksuwannatorn)"
        self.fields['cnt_guard_amt'].initial = 0
        self.fields['cnt_sale_amt'].initial = 0

