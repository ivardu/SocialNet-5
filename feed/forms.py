from django import forms
from feed.models import Feed, Likes, Comments

class FeedForm(forms.ModelForm):
	post = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':"What's on your mind today", 'class':'small'}))
	image = forms.ImageField(label='Upload Photos')
	class Meta:
		model = Feed
		fields = ['post','image']


class LikesForm(forms.ModelForm):

	class Meta:
		model = Likes
		fields = ['likes']

class CommentsForm(forms.ModelForm):
	comment = forms.CharField(label ='', widget=forms.TextInput(attrs={'placeholder':'Enter your comment', 'class':'form-control small'}))
	class Meta:
		model = Comments
		fields = ['comment']