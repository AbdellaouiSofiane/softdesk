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


class Issue(models.Model):
	TAG_CHOICES = (
		('bug', 'bug'),
		('improvement', 'improvement'),
		('task', 'task')
	)

	PRIORITY_CHOICES = (
		('low', 'low'),
		('average', 'average'),
		('high', 'high')
	)

	STATUS_CHOICES = (
		('todo', 'todo'),
		('in progress', 'in progress'),
		('done', 'done')
	)

	project = models.ForeignKey(Project,
		on_delete=models.CASCADE, related_name='issues')
	author = models.ForeignKey(settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE, related_name="owned_issues")
	assignee = models.ForeignKey(settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE, related_name="assigned_issues")

	title = models.CharField(max_length=255)
	description = models.CharField(max_length=1023)
	tag = models.CharField(max_length=20, choices=TAG_CHOICES)
	priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)
	created_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"issue: {self.title}"
