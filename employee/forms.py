from django import forms
from django.contrib.auth.models import User
from employee.models import Profile

class UserForm(forms.ModelForm):
	username=forms.CharField(help_text=None)
	password=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=['username', 'first_name', 'last_name' ,'email', 'password']
		label={'password':'Password'}


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['username', 'first_name', 'last_name' ,'email']
		

class UserLoginForm(forms.Form):
	username=forms.CharField(help_text = '')
	password=forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model=User
		fields=['username', 'password']

class ProfileForm(forms.ModelForm):
	class Meta:
		model=Profile
		fields=['role_type', 'designation','salary']