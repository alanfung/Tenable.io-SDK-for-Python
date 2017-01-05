from nessus.exceptions import NessusErrorCode, NessusException
from tests.base import BaseTest


class TestNessusException(BaseTest):

    def test_default_error_code_not_none(self):
        exception = NessusException()
        assert exception.code is not None, u'There should always be a code.'
        exception2 = NessusException(code=None)
        assert exception2.code is not None, u'Error code is never None even if None is passed as code in constructor.'

    def test_default_error_code_is_generic(self):
        exception = NessusException()
        assert exception.code is NessusErrorCode.GENERIC, u'Default error code should be generic.'


class TestNessusErrorCode(BaseTest):

    def test_from_http_code(self):
        assert NessusErrorCode.from_http_code(404) is not None, u'Error code found for 404 http status code.'
        assert NessusErrorCode.from_http_code(429) is NessusErrorCode.TOO_MANY_REQUESTS, \
            u'Error code "TOO MANY REQUEST" is found for 429 http status code.'
