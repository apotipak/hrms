from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from django.utils.translation import ugettext_lazy as _


language_options = {
	('en','English US'), ('th','Thai')
}


class ChangePasswordForm(ModelForm):
	password = forms.CharField(max_length=128, error_messages={'required': 'กรุณาป้อนรหัสผ่านเก่า'}, widget=forms.PasswordInput(attrs={'autocomplete':'off'}))
	new_password = forms.CharField(max_length=128, error_messages={'required': 'กรุณาป้อนรหัสผ่านใหม่'}, widget=forms.TextInput(attrs={'autocomplete':'off'}))
	confirm_new_password = forms.CharField(max_length=128, error_messages={'required': 'กรุณาป้อนรหัสผ่านใหม่อีกครั้ง'}, widget=forms.TextInput(attrs={'autocomplete':'off'}))

	class Meta:
		model = User
		fields = ['password']

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		self.confirm_new_password = kwargs.pop('confirm_new_password', None)
		super(ChangePasswordForm, self).__init__(*args, **kwargs)
		self.fields['password'].widget.attrs = {'class': 'form-control col-12'}
		self.fields['password'].widget.attrs['placeholder'] = _("Enter old password")
		self.fields['new_password'].widget.attrs = {'class': 'form-control col-12'}
		self.fields['new_password'].widget.attrs['placeholder'] = _("Enter new password")
		self.fields['confirm_new_password'].widget.attrs = {'class': 'form-control col-12'}
		self.fields['confirm_new_password'].widget.attrs['placeholder'] = _("Reenter new password")

	def clean(self):
		cleaned_data = super(ChangePasswordForm, self).clean()
		username = self.user.username
		password = self.cleaned_data.get('password')
		new_password = self.cleaned_data.get('new_password')
		confirm_new_password = self.cleaned_data.get('confirm_new_password')		
		userobj = User.objects.get(username=username)

		if userobj.check_password(password):
			if re.match(r"^(?=.*[\d])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", new_password):							
				if new_password != confirm_new_password:
					raise forms.ValidationError(_("New password is not same."))
				else:
					if new_password == password:
						raise forms.ValidationError(_("New password is same as the old one."))
					else:
						return cleaned_data

			else:
				raise forms.ValidationError(_("รหัสใหม่ควรยาวอย่างน้อย 6 ตัวอักษร และประกอบด้วย ตัวเลข ตัวหนังสือ สัญลักษณ์"))

		else:
			raise forms.ValidationError(_("Enter incorrect old password."))

		return cleaned_data


class LanguageForm(ModelForm):
	language_code = forms.CharField(label=_('Select your default language'), max_length=2, widget=forms.Select(choices=language_options))

	class Meta:
		model = UserProfile
		fields = ['language_code']

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(LanguageForm, self).__init__(*args, **kwargs)
		self.fields['language_code'].widget.attrs={'class': 'form-control'}
		if UserProfile.objects.filter(employee_id=self.user.username).exists():
			default_language = UserProfile.objects.filter(employee_id=self.user.username).values_list('language_code', flat=True).get()			
		else:
			default_language = 'th'
		self.initial['language_code'] = default_language

	def clean(self):
		cleaned_data = super(LanguageForm, self).clean()
		language_code = self.data.get('language_code')
		if language_code not in ('en', 'th'):
			raise forms.ValidationError(_("Invalid value"))
		return cleaned_data
