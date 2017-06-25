from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics


class Root(APIView):

	def get(self, request):
		return Response({
			"name": "Django Annotator Store",
			"version": "0.0.1",
		})


from .models import Annotation
from .serializers import AnnotationSerializer
from . import mixins
from rest_framework.permissions import IsAuthenticated

class AnnotationList(generics.ListAPIView, mixins.CreateModelMixin):

	queryset = Annotation.objects.all()
	serializer_class = AnnotationSerializer
	permission_classes = (IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		# print(request.data)
		return self.create(request, *args, **kwargs)

	# def initial(self, request, *args, **kwargs):
	# 	"""
	# 	Runs anything that needs to occur prior to calling the method handler.
	# 	"""
	# 	self.format_kwarg = self.get_format_suffix(**kwargs)
	#
	# 	print('REQUEST ----', request.data)
	# 	# Perform content negotiation and store the accepted info on the request
	# 	neg = self.perform_content_negotiation(request)
	# 	request.accepted_renderer, request.accepted_media_type = neg
	#
	# 	# Determine the API version, if versioning is in use.
	# 	version, scheme = self.determine_version(request, *args, **kwargs)
	# 	request.version, request.versioning_scheme = version, scheme
	#
	# 	# Ensure that the incoming request is permitted
	# 	self.perform_authentication(request)
	# 	self.check_permissions(request)
	# 	self.check_throttles(request)
	# 	print('authentication success')


class AnnotationDetail(generics.RetrieveDestroyAPIView, mixins.UpdateModelMixin):

	queryset = Annotation.objects.all()
	serializer_class = AnnotationSerializer
	permission_classes = (IsAuthenticated,)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	# Don't know if useful
	def patch(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)


from .pagination import SearchPagination

class SearchView(generics.ListAPIView):

	queryset = Annotation.objects.all()
	serializer_class = AnnotationSerializer
	pagination_class = SearchPagination
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		queryset = self.queryset
		uri = self.request.GET['uri']
		return queryset.all().filter(uri=uri)


import jwt, datetime
from django.contrib.auth.decorators import login_required # FIXME

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
