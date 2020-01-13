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


	def __str__(self):
		return self.user.username + " Post"

	def save(self):
		super().save()
		img = Image.open(self.image.path)

		if img.height > 400 and img.width > 400:
			output = (400,400)
			img.thumbnail(output)
			img.save(self.image.path)