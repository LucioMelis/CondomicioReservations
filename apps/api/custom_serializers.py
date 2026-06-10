from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.serializers import ModelSerializer

import logging

from apps.api.exceptions import APICustomException

logger = logging.getLogger(__name__)

class CommonSerializer(ModelSerializer):
    _KEY_OBJECT = 'object'
    _KEY_ATTRIBUTE = 'attribute'
    _KEY_SERIALIZER = 'serializer'
    _KEY_DATA = 'data'
    _TYPE_OF_FILE = 'type'

    def __init__(self, *args, **kwargs):
        super(CommonSerializer, self).__init__(*args, **kwargs)
        self.user = None
        self.request = None

    def pack_object_item(self, attribute, object_instance, serializer, data):
        return {
            self._KEY_ATTRIBUTE: attribute,
            self._KEY_OBJECT: object_instance,
            self._KEY_SERIALIZER: serializer,
            self._KEY_DATA: data
        }

    def unpack_object_item(self, object_item):
        return (
            object_item.get(self._KEY_ATTRIBUTE),
            object_item.get(self._KEY_OBJECT),
            object_item.get(self._KEY_SERIALIZER),
            object_item.get(self._KEY_DATA)
        )

    def get_request(self, context=None):
        if not self.request:
            try:
                _context = context
                if not _context:
                    _context = self.context
                self.request = _context.get('request')
            except Exception as e:
                logger.exception('Error during get request object from serializer: ', exc_info=e)
        return self.request

    def _get_user_request(self, context=None):
        if not self.user:
            try:
                request = self.get_request(context)
                self.user = request.user
            except Exception as e:
                logger.exception('Error during get user request object from serializer: ',exc_info=e)
        return self.user

    def get_user(self, context=None, raise_exception=True):
        user = self._get_user_request(context)
        if not isinstance(user, get_user_model()) and raise_exception:
            msg = 'Request with user must be set to serializer'
            logger.exception('WARNING: %s' % (msg,))
            raise APICustomException(msg, 'serializer_without_user_or_request',None,status.HTTP_500_INTERNAL_SERVER_ERROR)
        return user

    def get_access_type(self, context=None):
        try:
            _context = context
            if not _context:
                _context = self.context
            _access_type = _context.get('access_type')
            if _access_type is not None:
                self.access_type = _access_type
        except Exception as e:
            logger.exception('Error during get access type from serializer: ', exc_info=e)
        return self.access_type

    def create_absolute_url(self, url):
        request = self.get_request()
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    def create_serializer_context(self):
        return {'context': self.context}

    def set_content_file_type(self, file_type):
        srz_context = self.create_serializer_context()
        if srz_context and srz_context.get('context'):
            srz_context['context'][CommonSerializer._TYPE_OF_FILE] = file_type
        else:
            srz_context = {'context': {CommonSerializer._TYPE_OF_FILE: file_type}}
        return srz_context

    def modify_internal_value_data(self, data):
        return data

    def run_extra_validation_and_data(self, attrs):
        return attrs

    def to_internal_value(self, data):
        modified_data = self.modify_internal_value_data(data)
        return super(CommonSerializer, self).to_internal_value(modified_data)

    def validate(self, attrs):
        if attrs is None:
            return super(CommonSerializer, self).validate(attrs)
        attrs = self.run_extra_validation_and_data(attrs)
        return super(CommonSerializer, self).validate(attrs)

    def _save_related_object(self, instance, related_object, related_serializer, data, srz_context):
        partial = True if related_object else False
        _serializer = related_serializer(related_object, data, partial=partial, **srz_context)
        _serializer.is_valid(raise_exception=True)
        _child_updated = _serializer.save()
        return _child_updated

    def _handle_related_object(self, instance, child_item, srz_context):
        related_attribute, related_object, related_serializer, data = self.unpack_object_item(
            child_item)
        related_object = self._save_related_object(instance, related_object,
                                                   related_serializer, data, srz_context)
        return related_attribute, related_object

    def serialize_if_instance_exists(self, obj, serializer_class, many=False, *args, **kwargs):
        srz_context = self.create_serializer_context()
        srz_context.update(**kwargs)
        serializer = serializer_class(obj, many=many, **srz_context)
        return serializer.data if serializer.instance else None


class CommonModelParentRelatedSerializer(CommonSerializer):
    def __init__(self, *args, **kwargs):
        super(CommonModelParentRelatedSerializer, self).__init__(*args, **kwargs)
        self.parent_objects = None

    def get_parents_object(self, instance):
        return None

    def handle_save_parent_related_object(self, instance):
        parents = self.get_parents_object(instance)
        if isinstance(parents, list):
            self.parent_objects = list()
            srz_context = self.create_serializer_context()
            for parent_item in parents:
                parent_attribute, parent_object = self._handle_related_object(instance, parent_item, srz_context)
                self.parent_objects.append(parent_object)

    def delete_parent_objects(self):
        if isinstance(self.parent_objects, list):
            for child in self.parent_objects:
                child.delete()

    def is_valid(self, raise_exception=False):
        try:
            return super(CommonModelParentRelatedSerializer, self).is_valid(raise_exception=raise_exception)
        except Exception as e:
            self.delete_parent_objects()
            if raise_exception:
                raise e


class CommonModelChildRelatedSerializer(CommonSerializer):
    def __init__(self, *args, **kwargs):
        super(CommonModelChildRelatedSerializer, self).__init__(*args, **kwargs)
        self.required_child_objects = None

    def default_creation_of_child_object(self, instance, attribute, model):
        child_instance = None
        try:
            child_instance = getattr(instance, attribute)
        except Exception as e:
            logger.debug('Error creating child, maybe does not exist the attribute or the object, exception: %s' % (e,))
        if child_instance is None:
            child_instance = model()
        return child_instance

    def get_child_objects(self, instance):
        return None

    def get_required_child_objects(self, data):
        return None

    def handle_save_child_related_objects(self, instance):
        childs = self.get_child_objects(instance)
        if isinstance(childs, list):
            srz_context = self.create_serializer_context()
            for child_item in childs:
                child_attribute, child_object = self._handle_related_object(instance, child_item, srz_context)
                setattr(instance, child_attribute, child_object)
            instance.save()

    def handle_create_required_child_related_objects(self, data):
        childs = self.get_required_child_objects(data)
        if isinstance(childs, list):
            self.required_child_objects = list()
            srz_context = self.create_serializer_context()
            for child_item in childs:
                child_attribute, child_object = self._handle_related_object(None, child_item, srz_context)
                data[child_attribute] = child_object.pk
                self.required_child_objects.append(child_object)
        return data

    def modify_internal_value_data(self, data):
        data = super(CommonModelChildRelatedSerializer, self).modify_internal_value_data(data)
        data = self.handle_create_required_child_related_objects(data)
        return data

    def delete_required_child_objects(self):
        if isinstance(self.required_child_objects, list):
            for child in self.required_child_objects:
                child.delete()

    def is_valid(self, raise_exception=False):
        try:
            return super(CommonModelChildRelatedSerializer, self).is_valid(raise_exception=raise_exception)
        except Exception as e:
            self.delete_required_child_objects()
            if raise_exception:
                raise e


class BaseModelSerializer(CommonModelParentRelatedSerializer, CommonModelChildRelatedSerializer):
    def save(self, **kwargs):
        try:
            with transaction.atomic():
                self.handle_save_child_related_objects(self.instance)
                instance = super(BaseModelSerializer, self).save(**kwargs)
                self.handle_save_parent_related_object(instance)
                return instance
        except Exception as e:
            self.delete_required_child_objects()
            self.delete_parent_objects()
            raise e