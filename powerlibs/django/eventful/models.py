import inspect

from django.db import models
from django.db import transaction

from .managers import EventfulManager


class EventfulModelMixin:
    def get_context(self, **kwargs):
        force_insert = kwargs.get('force_insert', False)

        the_context = {
            'is_creation': (self.id is None or force_insert is True),
        }
        the_context.update(kwargs)

        return the_context

    def trigger_event(self, event_name, **context):
        for attribute in dir(self):
            if attribute.startswith(event_name):
                method = getattr(self, attribute)
                if inspect.ismethod(method):
                    method(**context)

    def save(self, *args, **kwargs):
        force_insert = kwargs.get('force_insert', False)
        context = self.get_context(force_insert=force_insert)

        if context['is_creation']:
            super().save(*args, **kwargs)
        else:
            with transaction.atomic():
                self.trigger_event('pre_update', **context)
                super().save(*args, **kwargs)
                self.trigger_event('post_update', **context)

    def delete(self, *args, **kwargs):
        context = self.get_context()

        with transaction.atomic():
            self.trigger_event('pre_delete', **context)
            super().delete(*args, **kwargs)
            self.trigger_event('post_delete', **context)


class EventfulModel(EventfulModelMixin, models.Model):
    class Meta:
        abstract = True

    objects = EventfulManager()
