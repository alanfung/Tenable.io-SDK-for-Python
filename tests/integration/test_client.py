from nessus.client import NessusClient
from nessus.exceptions import NessusApiException, NessusErrorCode
from tests.base import BaseTest


class TestNessusClient(BaseTest):

    def test_client_bad_keys(self):
        try:
            NessusClient('bad', 'key').session_api.get()
            assert False, u'NessusApiException should be raised for bad api and secret keys.'
        except NessusApiException as e:
            assert e.code is NessusErrorCode.UNAUTHORIZED, u'Appropriate exception is raised.'
