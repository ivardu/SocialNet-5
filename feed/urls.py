from django.urls import path
from feed import views as feed_views

app_name = 'feed'
urlpatterns = [
	path('', feed_views.HomePageView.as_view(), name='home'),
	path('feed/',feed_views.feed_list, name='feed_list'),
]