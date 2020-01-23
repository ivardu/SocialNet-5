from users.models import SnetUser, GENDER_CHOICES, Profile, Friends
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
	gender = forms.ChoiceField(choices=GENDER_CHOICES)
	email = forms.CharField(label='Email')
	first_name = forms.CharField()
	last_name = forms.CharField()

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
	# Need to create the custom third party date picker
	dob = forms.DateField(widget=forms.TextInput(attrs={
			'id':'datepicker',
		}))

	class Meta:
		model = SnetUser
		fields = ['username','first_name','last_name','dob','email','gender']
		help_texts = {
			'username': None,
		}



class ProfileForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['image']


class UserUpdateForm(forms.ModelForm):
	dob = forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker', }))

	class Meta:
		model = SnetUser
		fields = ['first_name','last_name', 'dob', 'email']


class FriendsReqForm(forms.ModelForm):

	class Meta:
		model = Friends
		fields = ['f_req']

class FriendsForm(forms.ModelForm):

	class Meta:
		model = Friends 
		fields = ['frnds']