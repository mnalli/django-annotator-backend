from django.db import models
from django.contrib.auth.models import User

import json, uuid

from django.urls import reverse
from jsonfield import JSONField

class Annotation(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular annotation")
	user = models.ForeignKey(User, db_index=True, blank=True, null=True)
	# user = models.CharField(max_length=100, null=True)
	# datetime in iso8601
	created = models.DateTimeField(auto_now_add=True, db_index=True)
	updated = models.DateTimeField(auto_now=True, db_index=True)

	text = models.TextField()
	quote = models.TextField()
	# is 200 sufficient for uri lenght?
	# relative uri (whithout domain name)
	uri = models.CharField(max_length=200, null=True)
	ranges = JSONField(null=True)
	permissions = JSONField(null=True)

	class Meta:
		ordering = ["-created"]


	def get_absolute_url(self):
		return reverse('annotator.annotation', args=[str(self.id)])

	def __str__(self):
		# FIXME
		return str(self.id)
