from django.db import models
from django.contrib.auth.models import AbstractUser

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