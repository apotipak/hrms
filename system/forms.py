from django import forms
from .models import TAprove

class CompanyApprovePriorityForm(forms.ModelForm):
    class Meta:
        model = TAprove
        fields = ('apr_id', 'apr_name_th', 'apr_pos_th', 'apr_piority', )

    """
    def __init__(self, *args, **kwargs):
    	super(CompanyApprovePriorityForm, self).__init__(*args, **kwargs)
    	self.fields['apr_id'].label = "Approve ID"
    	self.fields['apr_name_th'].label = "Name (TH)"
    	self.fields['apr_pos_th'].label = "Position (TH)"
    	self.fields['apr_piority'].label = "Priority Type"    	
	"""
	
