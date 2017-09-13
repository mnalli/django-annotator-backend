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
		return self.create(request, *args, **kwargs)


class AnnotationDetail(generics.RetrieveAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):

	queryset = Annotation.objects.all()
	serializer_class = AnnotationSerializer
	permission_classes = (IsAuthenticated,)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	# Don't know if useful
	def patch(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


from .pagination import SearchPagination

class SearchView(generics.ListAPIView):

	queryset = Annotation.objects.all()
	serializer_class = AnnotationSerializer
	pagination_class = SearchPagination
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		queryset = self.queryset
		applicant = self.request.user
		# selecting annotation from current document
		uri = self.request.GET['uri']
		notpurged = queryset.all().filter(uri=uri)
		# checking permissions
		return self.permission_filter(notpurged, applicant.pk)

	@classmethod
	def permission_filter(cls, queryset, applicant_pk):
		filtered_queryset = []
		for annotation in queryset:
			# check if the applicant has read permission
			read_permission_owners = annotation.permissions['read']
			if cls.can_view(read_permission_owners, applicant_pk):
				filtered_queryset += [annotation]
		return filtered_queryset

	@staticmethod
	def can_view(read_permission_owners, applicant_pk):
		if read_permission_owners:
			return applicant_pk in read_permission_owners
		else:
			return True
