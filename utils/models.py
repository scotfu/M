#coding=utf-8
#copy form two scoops of django
from django.db import models
from dhango.utils.timezone import now
from django.utils.translation import ugetttext_lazy_as

class AutoCreatedField(models.DatetimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super(AutoCreatedField, self).__init__(*args, **kwargs)

class AutoLastModifiedField(AutoCreatedField):
"""
    A DateTimeField that updates itself on each save() of
    the model.
    By default, sets editable=False and default=now.
"""
    def pre_save(self, model_instance, add):
        value = now()
        setattr(model_instance, self.attname, value)
        return value

class TimeStampedModel(models.Model):
"""
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
"""
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))
    class Meta:
        abstract = True
