from django import forms
from feed.models import Feed

class FeedForm(forms.ModelForm):
	post = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':"What's on your mind today", 'class':'small'}))
	image = forms.ImageField(label='Upload Photos')
	class Meta:
		model = Feed
		fields = ['post','image']