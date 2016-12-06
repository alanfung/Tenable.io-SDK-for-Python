import pytest
import six

if six.PY34:
    import unittest.mock as mock
else:
    import mock

from nessus.client import NessusClient, NessusException, NessusRetryableException


class TestNessusClient(object):

    def test_client_retries(self):

        # Function that throws NessusRetryableException
        mock_response = mock.Mock()
        foo = mock.Mock(side_effect=NessusRetryableException(mock_response))

        # Function decoration
        retried_foo = NessusClient._retry(foo)

        with pytest.raises(NessusException):
            retried_foo()

        assert foo.call_count == 4, u'Should be tried 4 times (retried 3 times).'

    def test_client_throwing_retryable_exception(self):

        responses = [
            [{'status_code': 200}, False],
            [{'status_code': 429}, True],
            [{'status_code': 501}, True],
            [{'status_code': 502}, True],
            [{'status_code': 503}, True],
        ]

        # Function that returns Responses with above status codes.
        foo = mock.Mock(side_effect=[mock.Mock(**response[0]) for response in responses])

        # Method decoration
        foo = NessusClient._error_handler(foo)

        for (response, retry) in responses:
            print (response, retry)
            if retry:
                with pytest.raises(NessusRetryableException):
                    foo()
            else:
                try:
                    foo()
                except NessusRetryableException:
                    assert False, u'Response %s should not be retry-able.' % response