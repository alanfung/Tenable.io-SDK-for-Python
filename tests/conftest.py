import pytest
import uuid


class App:

    def __init__(self):
        self._uuid = uuid.uuid4()

    def session_name(self, name, length=8):
        return u'%s_%s' % (name, self._uuid.hex[:length])


@pytest.fixture(scope='session')
def app():
    yield App()
