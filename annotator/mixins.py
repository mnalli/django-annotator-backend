"""
The mixins defined in this module are the same as rest_framework's mixins
except for the fact that they returns on success HTTP 303 SEE OTHER.
The redirecting url to the resource will be in the headers of the response.
"""

from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status

class CreateModelMixin(object):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(instance)
        return Response(serializer.data, status=status.HTTP_303_SEE_OTHER, headers=headers)

    def perform_create(self, serializer):
        "Returns the instance of the created model."
        return serializer.save()

    def get_success_headers(self, instance):
        return {'Location': instance.get_absolute_url()}


class UpdateModelMixin(object):
    """
    Update a model instance.
    """

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

        headers = self.get_success_headers(instance)
        return Response(serializer.data, status=status.HTTP_303_SEE_OTHER, headers=headers)

    def perform_update(self, serializer):
        "Returns the instance of the created model."
        return serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_success_headers(self, instance):
        return {'Location': instance.get_absolute_url()}
