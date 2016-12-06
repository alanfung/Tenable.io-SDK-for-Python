import pytest

from nessus.client import NessusClient, NessusException


class TestNessusClient(object):

    def test_client_bad_keys(self):
        with pytest.raises(NessusException):
            NessusClient('bad', 'key').session.get()
