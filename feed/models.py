from django.db import models
from users.models import SnetUser
from PIL import Image
from datetime import datetime, timedelta, timezone

# Create your models here.

def feed_data_directory(instance, filename):
	return f'{instance.user.username}/{filename}'

class Feed(models.Model):
	post = models.CharField(max_length=255)
	image = models.ImageField(upload_to=feed_data_directory)
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(SnetUser, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-date']
		


	def __str__(self):
		return self.user.username + " Post"

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.image.path)

		if img.height > 400 and img.width > 400:
			output = (400,400)
			image = img.resize(output, Image.ANTIALIAS)
			image.save(self.image.path)

	def post_time(self):
		current_time = datetime.now(timezone.utc)
		post_time = self.date
		display_time = current_time-post_time

		if display_time.days >=30 and display_time.days <= 365:
			if display_time.days//30:
				return f"{display_time.days//30} month ago"
			else:
				return f"{display_time.days//30} months ago"

		elif display_time.days >=1 and display_time.days <30:
			if display_time.days == 1:
				return f"{display_time.days} day ago"
			else:
				return f"{display_time.days} days ago"

		elif ((display_time.seconds)/60) <=59 and ((display_time.seconds)/60) >=1:
			return f"{(display_time.seconds)//60} minutes ago"

		elif (display_time.seconds)/60 >= 60:
			return f"{round(((display_time.seconds)/60)/60)} hours ago"

		else:
			return f"{display_time.seconds} seconds ago"

		return f"{display_time.days//365} years ago"


class Likes(models.Model):
	likes = models.IntegerField()
	post = models.ForeignKey(Feed, on_delete=models.CASCADE)
	user = models.ForeignKey(SnetUser, on_delete=models.CASCADE)


	def __str__(self):
		return self.user.username

class Comments(models.Model):
	comment = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now_add=True)
	post = models.ForeignKey(Feed, on_delete=models.CASCADE)
	user = models.ForeignKey(SnetUser, on_delete=models.CASCADE)

	def __str__(self):
		return self.comment

	class Meta:
		ordering = ['-date']