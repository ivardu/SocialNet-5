from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from users.forms import SignUpForm, ProfileForm, UserUpdateForm
from users.models import SnetUser


# SignUP Class view

class SignupFormView(FormView):
	template_name = 'users/signup.html'
	form_class = SignUpForm
	success_url = reverse_lazy('login')

	def form_valid(self, form):
		form.save()

		return super().form_valid(form)

# Profile Creation View
def profile(request):

	if request.method == 'POST':
		# Display the details of the form from the DB when you pass an instance
		p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		u_form = UserUpdateForm(request.POST, instance=request.user)
		if p_form.is_valid() and u_form.is_valid():
			p_form.save()
			u_form.save()

			return HttpResponseRedirect(reverse('profile'))

	else:
		# As I don't want to display the existing user details
		p_form = ProfileForm()
		u_form = UserUpdateForm(instance=request.user)

	return render(request, 'users/profile.html', locals())


def rprofile(request, pk):
	ruser = SnetUser.objects.get(pk=pk)
	form = UserUpdateForm(instance=ruser)

	return render(request, 'users/rprofile.html', locals())