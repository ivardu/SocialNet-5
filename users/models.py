from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

# Create your models here.
GENDER_CHOICES = (
		('M', 'Male'),
		('F','Female'),
		('O','Others'),
	)


class SnetUser(AbstractUser):

	dob = models.DateField()
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


	def __str__(self):

		return self.first_name+" "+self.last_name


def profile_pic_dir(instance, filename):
	return f'{instance.user.username}/profile_pics/{filename}'

class Profile(models.Model):
	image = models.ImageField(default='default.png', upload_to=profile_pic_dir) 
	user = models.OneToOneField(SnetUser, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username +" "+Profile


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.image.path)
		if img.height>150 and img.width>150:
			output=(150,150)
			img = img.resize(output, Image.ANTIALIAS)
			img.save(self.image.path)
