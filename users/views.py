from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from users.forms import SignUpForm, ProfileForm, UserUpdateForm, FriendsReqForm, FriendsForm
from users.models import SnetUser, Friends
from django.db.models import Q


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
		fracp = Friends.objects.filter(frnds='no').filter(auser=request.user)

	return render(request, 'users/profile.html', locals())


def rprofile(request, pk):
	auser = SnetUser.objects.get(pk=pk)
	form = UserUpdateForm(instance=auser)
	fr_form = FriendsForm()

	try:
		fracp = Friends.objects.filter(f_req='yes').filter(auser=auser).filter(ruser=request.user)
		frreq = Friends.objects.filter(f_req='yes').filter(ruser=auser).filter(auser=request.user)
		if fracp:
			fracp = fracp[0]
		if frreq:
			frreq = frreq[0]
	except:
		return render(request, 'users/rprofile.html', locals())

	return render(request,'users/rprofile.html', locals())


def friend_request(request, pk):

	if request.method == 'POST':
		fr_form = FriendsReqForm(request.POST)
		frndsform = FriendsForm(request.POST)
		auser = SnetUser.objects.get(pk=pk)
		if fr_form.is_valid():
			fr_model_obj = fr_form.save(commit=False)
			fr_model_obj.ruser = request.user
			fr_model_obj.auser = auser
			fr_model_obj.save()
						
			return HttpResponseRedirect(reverse('rprofile', args=(pk,)))

		# print(request.POST.get('frnds'))
		
		if request.POST.get('frnds',1) != 1:
			frnd = Friends.objects.filter(ruser=auser).get(auser=request.user)
			frnd.frnds = request.POST['frnds']
			frnd.save()

			return HttpResponseRedirect(reverse('rprofile', args=(pk,)))



def friends_list(request):

	frnd_req = Friends.objects.filter(frnds='no').filter(auser=request.user)
	frnd_list = Friends.objects.filter(frnds='yes').filter(Q(ruser=request.user) | Q(auser=request.user))
	print(frnd_list)

	return render(request, 'users/frnd_req.html', locals())


