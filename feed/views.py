from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from users.models import SnetUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from feed.models import Feed
from feed.forms import FeedForm


#Home Page View for the S_Net 5
class HomePageView(ListView):
	model = SnetUser
	template_name = 'feed/home.html'


#Feed List View for the S_NET 5

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
		if feed_form.is_valid():
			f_mod_obj = feed_form.save(commit=False)
			f_mod_obj.user = request.user
			f_mod_obj.save()

			return HttpResponseRedirect(reverse('feed:feed_list'))
	else:
		feed_form = FeedForm()

	return render(request, 'feed/feed.html', locals())



class MyPostView(ListView):
	model = Feed
	template_name = 'feed/myposts.html'
	paginate_by = 4


	def get_queryset(self):
		return Feed.objects.filter(user_id=self.kwargs['pk'])