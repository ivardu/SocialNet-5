from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from users.models import SnetUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from feed.models import Feed
from feed.forms import FeedForm, LikesForm, CommentsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


#Home Page View for the S_Net 5
class HomePageView(ListView):
	model = Feed
	template_name = 'feed/home.html'

	def get_queryset(self):
		return Feed.objects.all()[:1]


#Feed List View for the S_NET 5

@login_required
def feed_list(request):
	feed_obj = Feed.objects.all()
	paginator = Paginator(feed_obj, 5)
	page = request.GET.get('page',1)
	try:
		pages = paginator.page(page)

	except PageNotAnInteger:
		pages = paginator.page(1)

	except EmptyPage:
		pages = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		feed_form = FeedForm(request.POST, request.FILES)
		likes_form = LikesForm(request.POST)
		post_item = Feed.objects.get(pk=request.POST['post_id'])
		diff_user = post_item.likes_set.filter(user=request.user).count() and True or False
		comment_form = CommentsForm(request.POST)
		if feed_form.is_valid():
			f_mod_obj = feed_form.save(commit=False)
			f_mod_obj.user = request.user
			f_mod_obj.save()

			return HttpResponseRedirect(reverse('feed:feed_list'))

		elif likes_form.is_valid() and diff_user == False:
			likes_model_obj = likes_form.save(commit=False)
			likes_model_obj.likes = likes_form.cleaned_data['likes']
			likes_model_obj.post = post_item
			likes_model_obj.user = request.user
			likes_model_obj.save()

			return HttpResponseRedirect(reverse('feed:feed_list'))

		elif comment_form.is_valid():
			comm_model_obj = comment_form.save(commit=False)
			comm_model_obj.post = post_item
			comm_model_obj.user = request.user
			print(comment_form)
			comm_model_obj.save()

			return HttpResponseRedirect(reverse('feed:feed_list'))

		else:
			return HttpResponseRedirect(reverse('feed:feed_list'))

	else:
		feed_form = FeedForm()
		comment_form = CommentsForm()



	return render(request, 'feed/feed.html', locals())


# @login_required
class MyPostView(LoginRequiredMixin, ListView):
	model = Feed
	template_name = 'feed/myposts.html'
	paginate_by = 4


	def get_queryset(self):
		return super(MyPostView, self).get_queryset().filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['comment'] = CommentsForm
		return context



class EditPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Feed
	template_name = 'feed/edit_post.html'
	form_class = FeedForm
	success_url= reverse_lazy('feed:myposts')

	def test_func(self): 
		return self.get_object().user == self.request.user
