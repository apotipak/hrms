from django import forms
from .models import TAprove
from .models import ComDepartment


class CompanyApprovePriorityCreateForm(forms.ModelForm):
    class Meta:
        model = TAprove
        fields = ('apr_id', 'apr_title', 'apr_name_th', 'apr_pos_th', 'apr_piority')
        error_messages = {
            'apr_id': {
                'required': "This field is required",
            }
        }

    def __init__(self, *args, **kwargs):
        super(CompanyApprovePriorityCreateForm, self).__init__(*args, **kwargs)
        self.fields['apr_id'].label = "Approve ID"
        self.fields['apr_title'].label = "Title"
        self.fields['apr_name_th'].label = "Name (TH)"
        self.fields['apr_pos_th'].label = "Position (TH)"
        self.fields['apr_piority'].label = "Priority Type"


class CompanyApprovePriorityUpdateForm(forms.ModelForm):
    class Meta:
        model = TAprove
        fields = ('apr_id', 'apr_title', 'apr_name_th', 'apr_pos_th', 'apr_piority', )

    def __init__(self, *args, **kwargs):
        super(CompanyApprovePriorityUpdateForm, self).__init__(*args, **kwargs)
        self.fields['apr_id'].widget.attrs['readonly'] = True
        self.fields['apr_id'].label = "Approve ID"
        self.fields['apr_title'].label = "Title"
        self.fields['apr_name_th'].label = "Name (TH)"
        self.fields['apr_pos_th'].label = "Position (TH)"
        self.fields['apr_piority'].label = "Priority Type"

        
    def clean_apr_id(self):
        if self.instance: 
            return self.instance.apr_id
        else: 
            return self.fields['apr_id']


class CompanyDepartmentForm(forms.ModelForm):
    class Meta:
        model = ComDepartment
        fields = ('dept_id', 'div_id', 'dept_sht', 'dept_th', 'dept_en', 'dept_zone')

    def __init__(self, *args, **kwargs):
    	super(CompanyDepartmentForm, self).__init__(*args, **kwargs)
    	self.fields['dept_id'].label = "Department ID"
    	self.fields['div_id'].label = "Division ID"
    	self.fields['dept_sht'].label = "Description Short Info"
    	self.fields['dept_th'].label = "Description (TH)"
    	self.fields['dept_en'].label = "Description (EN)"
    	self.fields['dept_zone'].label = "Department Zone"
