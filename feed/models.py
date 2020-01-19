from django.db import models
from users.models import SnetUser
from PIL import Image

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

		if img.height > 200 and img.width > 200:
			output = (200,200)
			img.thumbnail(output, Image.ANTIALIAS)
			img.save(self.image.path)


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