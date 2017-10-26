import inspect

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from powerlibs.django.restless.models import serialize_model


class EventfulModelMixin:
    def serialize(self):  # pragma: no cover
        return serialize_model(self)

    def get_context(self, **kwargs):
        force_insert = kwargs.get('force_insert', False)

        try:
            type(self).objects.get(pk=self.pk)
        except ObjectDoesNotExist:
            exists_on_database = False
        else:
            exists_on_database = True

        the_context = {
            'is_creation': (not exists_on_database or force_insert is True),
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

        with transaction.atomic():
            if context['is_creation']:
                self.trigger_event('pre_creation', is_creation=True)
                super().save(*args, **kwargs)
                self.trigger_event('post_creation', is_creation=True)
            else:
                self.trigger_event('pre_update', **context)
                super().save(*args, **kwargs)
                self.trigger_event('post_update', **context)

    def delete(self, *args, **kwargs):
        context = self.get_context()

        with transaction.atomic():
            self.trigger_event('pre_delete', **context)
            super().delete(*args, **kwargs)
            self.trigger_event('post_delete', **context)
