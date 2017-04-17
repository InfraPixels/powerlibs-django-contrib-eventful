from uuid import uuid4

from powerlibs.django.contrib.eventful.models import EventfulModelMixin


class Model:
    def __init__(self, **kwargs):
        self.id = None
        self.pk = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self, *args, **kwargs):
        self.id = self.pk = uuid4()

    def delete(self, *args, **kwargs):
        pass


class EventfulModel(EventfulModelMixin, Model):
    def __init__(self, *args, **kwargs):
        self.debug_info = {
            'pre_creation_handler_called': 0,
            'post_creation_handler_called': 0,
            'pre_update_handler_called': 0,
            'post_update_handler_called': 0,
            'pre_delete_handler_called': 0,
            'post_delete_handler_called': 0,
        }
        super().__init__(*args, **kwargs)

    def pre_creation_test(self, **context):
        self.debug_info['pre_creation_handler_called'] += 1

    def post_creation_test(self, **context):
        self.debug_info['post_creation_handler_called'] += 1

    def pre_update_test(self, **context):
        self.debug_info['pre_update_handler_called'] += 1

    def post_update_test(self, **context):
        self.debug_info['post_update_handler_called'] += 1

    def pre_delete_test(self, **context):
        self.debug_info['pre_delete_handler_called'] += 1

    def post_delete_test(self, **context):
        self.debug_info['post_delete_handler_called'] += 1
