from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from users.forms import SignUpForm, ProfileForm, UserUpdateForm, FriendReqForm
from users.models import SnetUser, FriendReq, FriendReqAcp


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

		# Friend Request Recieved details
		fracp = FriendReqAcp.objects.filter(friends='no').filter(auser=request.user)
		if fracp:
			fracp = fracp[0]
			freq = fracp.friendreq_set.all()

	return render(request, 'users/profile.html', locals())


def rprofile(request, pk):
	auser = SnetUser.objects.get(pk=pk)
	form = UserUpdateForm(instance=auser)
	fr_form = FriendReqForm()

	try:
		fracp = FriendReqAcp.objects.filter(friends='no').get(auser_id=auser.id)
		freq = fracp.friendreq_set.get(ruser=request.user)
	except:
		print('error')
		return render(request, 'users/rprofile.html', locals())

	return render(request,'users/rprofile.html', locals())


def friend_request(request, pk):

	if request.method == 'POST':
		fr_form = FriendReqForm(request.POST)
		auser = SnetUser.objects.get(pk=pk)
		if fr_form.is_valid():
			fracp = FriendReqAcp.objects.create(auser=auser)
			fr_model_obj = fr_form.save(commit=False)
			fr_model_obj.ruser = request.user
			fr_model_obj.save()
			fr_model_obj.fracp.add(fracp)
			
			return HttpResponseRedirect(reverse('rprofile', args=(pk,)))


