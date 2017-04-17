import pytest

from tests.factories import EventfulModel


@pytest.fixture
def eventful_model():
    return EventfulModel
