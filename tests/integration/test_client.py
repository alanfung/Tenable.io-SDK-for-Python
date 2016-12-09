import pytest

from nessus.client import NessusClient, NessusException
from tests.base import BaseTest


class TestNessusClient(BaseTest):

    def test_client_bad_keys(self):
        with pytest.raises(NessusException):
            NessusClient('bad', 'key').session.get()
