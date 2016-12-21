import pytest

from nessus.client import NessusClient, NessusApiException
from tests.base import BaseTest


class TestNessusClient(BaseTest):

    def test_client_bad_keys(self):
        with pytest.raises(NessusApiException):
            NessusClient('bad', 'key').session.get()
