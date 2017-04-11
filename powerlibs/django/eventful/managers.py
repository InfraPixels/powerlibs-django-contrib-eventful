from django.db import models
from django.db import transaction


class EventfulManager(models.Manager):
    def create(self, **kwargs):
        model_instance = self.model(**kwargs)
        with transaction.atomic():
            model_instance.trigger_event('pre_creation', is_creation=True)
            self.perform_create(model_instance, **kwargs)
            model_instance.trigger_event('post_creation', is_creation=True)
        return model_instance

    def perform_create(self, model_instance, **kwargs):
        model_instance.save(force_insert=True)
