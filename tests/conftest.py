import pytest
import uuid

from nessus.client import NessusClient


class App:

    def __init__(self):
        self._uuid = uuid.uuid4()

    def session_name(self, name, length=8):
        try:
            session_name = name % self._uuid.hex[:length]
        except TypeError:
            session_name = u'%s_%s' % (name, self._uuid.hex[:length])
        return session_name


@pytest.fixture(scope='session')
def app():
    yield App()


@pytest.fixture(scope='session')
def client():
    yield NessusClient()
