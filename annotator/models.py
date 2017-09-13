from django.db import models
from django.contrib.auth.models import User

import json, uuid

from django.urls import reverse
from jsonfield import JSONField

import uuid

class Document(models.Model):
	"""
	A document being annotated.

	Every document is created when the first annotation is created and deleted
	when the last annotation is deleted.
	"""

	title = models.CharField(primary_key=True, max_length=64, default=uuid.uuid1) # The title is unique
	revid = models.PositiveIntegerField(null=True)
	is_in_category = models.NullBooleanField()
	html_text = models.TextField()
	# the document is created with the first annotation
	number_of_annotations = models.PositiveIntegerField(default=1)

	def __str__(self):
		return self.title

class Annotation(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular annotation")
	# displayed by AnnotationSerializer as the primary key of the user
	user = models.ForeignKey(User, db_index=True, blank=True, null=True)
	# datetime in iso8601
	created = models.DateTimeField(auto_now_add=True, db_index=True)
	updated = models.DateTimeField(auto_now=True, db_index=True)

	# document = models.ForeignKey(Document, db_index=True, blank=True, null=True)
	# FIXME: Annotation and Document should be in a many to one relationship

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
