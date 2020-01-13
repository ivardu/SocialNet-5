from users.models import SnetUser, GENDER_CHOICES
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
	gender = forms.ChoiceField(choices=GENDER_CHOICES)
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
	# Need to create the custom third party date picker
	dob = forms.DateField(widget=forms.TextInput(attrs={
			'type':'date',
		}))

	class Meta:
		model = SnetUser
		fields = ['username','first_name','last_name','dob','gender']
		help_texts = {
			'username': None,
		}