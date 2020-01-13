from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import FormView
from users.forms import SignUpForm



class SignupFormView(FormView):
	template_name = 'users/signup.html'
	form_class = SignUpForm
	success_url = reverse_lazy('home')


	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

