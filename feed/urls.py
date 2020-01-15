from django.urls import path
from feed import views as feed_views

app_name = 'feed'
urlpatterns = [
	path('', feed_views.HomePageView.as_view(), name='home'),
	path('feed/',feed_views.feed_list, name='feed_list'),
	path('myposts/<int:pk>/',feed_views.MyPostView.as_view(), name='myposts'),
	path('edit/<int:pk>/',feed_views.EditPost.as_view(), name='edit'),
]