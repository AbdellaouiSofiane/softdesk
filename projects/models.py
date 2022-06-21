from django.conf import settings
from django.db import models


class Project(models.Model):
	TYPE_CHOICES = (
		('backend', 'backend'),
		('frontend', 'frontend'),
		('iOS', 'iOS'),
		('android', 'android')
	)

	title = models.CharField(max_length=255)
	description = models.CharField(max_length=1023)
	type = models.CharField(choices=TYPE_CHOICES, max_length=8)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE, related_name="owned_projects")
	contributors = models.ManyToManyField(settings.AUTH_USER_MODEL,
		related_name="contributing_projects")

	def __str__(self):
		return f"project: {self.title}"
