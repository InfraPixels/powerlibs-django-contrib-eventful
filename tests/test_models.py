import pytest

pytestmark = pytest.mark.django_db


def test_common_eventful_model_creation_with_create(eventful_model):
    obj = eventful_model(name='test 01')
    obj.save()

    assert obj.debug_info['pre_creation_handler_called'] == 1
    assert obj.debug_info['post_creation_handler_called'] == 1

    assert obj.debug_info['pre_update_handler_called'] == 0
    assert obj.debug_info['post_update_handler_called'] == 0

    assert obj.debug_info['pre_delete_handler_called'] == 0
    assert obj.debug_info['post_delete_handler_called'] == 0

    assert obj.pk is not None


def test_common_eventful_model_is_creation_context_value(eventful_model):
    obj = eventful_model(name='test 01')
    assert obj.get_context()['is_creation'] is True

    obj2 = eventful_model(name='test 02')
    obj2.id = 1
    assert obj.get_context()['is_creation'] is True


def test_common_eventful_model_update(eventful_model):
    obj = eventful_model(name='test 01')
    obj.save()

    obj.name = 'test 02'
    obj.save()

    assert obj.debug_info['pre_creation_handler_called'] == 1
    assert obj.debug_info['post_creation_handler_called'] == 1

    assert obj.debug_info['pre_update_handler_called'] == 1
    assert obj.debug_info['post_update_handler_called'] == 1

    assert obj.debug_info['pre_delete_handler_called'] == 0
    assert obj.debug_info['post_delete_handler_called'] == 0

    assert obj.get_context()['is_creation'] is False


def test_common_eventful_model_delete(eventful_model):
    obj = eventful_model(name='test 01')
    obj.save()
    obj.delete()

    assert obj.debug_info['pre_creation_handler_called'] == 1
    assert obj.debug_info['post_creation_handler_called'] == 1

    assert obj.debug_info['pre_update_handler_called'] == 0
    assert obj.debug_info['post_update_handler_called'] == 0

    assert obj.debug_info['pre_delete_handler_called'] == 1
    assert obj.debug_info['post_delete_handler_called'] == 1
