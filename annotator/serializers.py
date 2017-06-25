"""
An annotation is a JSON document that contains a number of fields describing the
position and content of an annotation within a specified document:
{

  "id": "39fc339cf058bd22176771b3e3187329",  # unique id (added by backend)
  "annotator_schema_version": "v1.0",        # schema version: default v1.0
  "created": "2011-05-24T18:52:08.036814",   # created datetime in iso8601 format (added by backend)
  "updated": "2011-05-26T12:17:05.012544",   # updated datetime in iso8601 format (added by backend)
  "text": "A note I wrote",                  # content of annotation
  "quote": "the text that was annotated",    # the annotated text (added by frontend)
  "uri": "http://example.com",               # URI of annotated document (added by frontend)
  "ranges": [                                # list of ranges covered by annotation (usually only one entry)
    {
      "start": "/p[69]/span/span",           # (relative) XPath to start element
      "end": "/p[70]/span/span",             # (relative) XPath to end element
      "startOffset": 0,                      # character offset within start element
      "endOffset": 120                       # character offset within end element
    }
  ],
  "user": "alice",                           # user id of annotation owner (can also be an object with an 'id' property)
  "consumer": "annotateit",                  # consumer key of backend
  "tags": [ "review", "error" ],             # list of tags (from Tags plugin)
  "permissions": {                           # annotation permissions (from Permissions/AnnotateItPermissions plugin)
    "read": ["group:__world__"],
    "admin": [],
    "update": [],
    "delete": []
  }
}
"""

from rest_framework import serializers
from django.contrib.auth.models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username',)
#
#
#
# class UsernameField(serializers.StringRelatedField):
#     def __init__(self, **kwargs):
#         kwargs['read_only'] = False
#         kwargs['queryset'] = User.objects.all()
#         super(serializers.StringRelatedField, self).__init__(**kwargs)
#
#     def to_internal_value(self, value):
#         return value

from .models import Annotation

class AnnotationSerializer(serializers.ModelSerializer):
    # annotator_schema_vision = "v1.0"
    ranges = serializers.JSONField()
    permissions = serializers.JSONField()
    # user = UsernameField()

    class Meta:
        model = Annotation
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')
        

    # def create(self, validated_data):
    #     print('SONO QUI----------------------------------')
    #     username = validated_data['user']
    #     validated_data['user'] = User.objects.get(username=username)
    #     annotation = Annotation.objects.create(**validated_data)
    #     return annotation
    #
    # def update(self, instance, validated_data):
    #     raise_errors_on_nested_writes('update', self, validated_data)
    #     info = model_meta.get_field_info(instance)
    #
    #     # Simply set each attribute on the instance, and then save it.
    #     # Note that unlike `.create()` we don't need to treat many-to-many
    #     # relationships as being a special case. During updates we already
    #     # have an instance pk for the relationships to be associated with.
    #     for attr, value in validated_data.items():
    #         if attr in info.relations and info.relations[attr].to_many:
    #             set_many(instance, attr, value)
    #         else:
    #             setattr(instance, attr, value)
    #     instance.save()
    #
    #     return instance
