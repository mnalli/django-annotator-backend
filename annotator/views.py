from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics

from django.urls import reverse


class Root(APIView):

	def get(self, request):
		return Response({
			"name": "Django Annotator Store",
			"version": "0.0.1",
		})


from .models import Annotation
from .serializers import AnnotationSerializer
from rest_framework import mixins

class AnnotationList(generics.ListAPIView):

	queryset = Annotation.objects.all()
	serializer_class = AnnotationSerializer


	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		instance = self.perform_create(serializer)
		headers = self.get_success_headers(instance.id)
		return Response(serializer.data, status=status.HTTP_303_SEE_OTHER, headers=headers)

	def perform_create(self, serializer):
		"Returns the instance of the created model."
		return serializer.save()

	def get_success_headers(self, pk):
		return {'Location': reverse('annotator.annotation', args=[pk])}


class AnnotationDetail(generics.RetrieveDestroyAPIView, mixins.UpdateModelMixin):

	queryset = Annotation.objects.all()
	serializer_class = AnnotationSerializer

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def patch(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
	   	# If 'prefetch_related' has been applied to a queryset, we need to
	   	# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		headers = self.get_success_headers(instance.id)
		return Response(serializer.data, status=status.HTTP_303_SEE_OTHER, headers=headers)

	def perform_update(self, serializer):
		"Returns the instance of the created model."
		return serializer.save()

	def partial_update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return self.update(request, *args, **kwargs)

	def get_success_headers(self, pk):
		return {'Location': reverse('annotator.annotation', args=[str(pk)])}


import jwt, datetime
from django.contrib.auth.decorators import login_required

class TokenView(APIView):

	# Replace these with your details
	CONSUMER_KEY = 'yourconsumerkey'
	CONSUMER_SECRET = 'yourconsumersecret'

	# Only change this if you're sure you know what you're doing
	CONSUMER_TTL = 86400

	@login_required
	def get(self, request):
		encoded_token = self.generate_token(request.user)
		print(encoded_token)
		return Response(encoded_token)

	@classmethod
	def generate_token(cls, user_id):
	    return jwt.encode({
	      'consumerKey': cls.CONSUMER_KEY,
	      'userId': user_id,
	      'issuedAt': _now().isoformat() + 'Z',
	      'ttl': cls.CONSUMER_TTL
	    }, cls.CONSUMER_SECRET)

	@staticmethod
	def _now():
	    return datetime.datetime.utcnow().replace(microsecond=0)
