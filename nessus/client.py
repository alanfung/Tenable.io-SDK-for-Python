import requests

from requests.utils import quote
from time import sleep

from nessus.config import NessusConfig
from nessus.exceptions import NessusException, NessusRetryableException
from nessus.api.asset_lists import AssetListsApi
from nessus.api.base import BaseRequest
from nessus.api.editor import EditorApi
from nessus.api.exclusions import ExclusionApi
from nessus.api.file import FileApi
from nessus.api.folders import FoldersApi
from nessus.api.groups import GroupsApi
from nessus.api.policies import PoliciesApi
from nessus.api.scans import ScansApi
from nessus.api.session import SessionApi
from nessus.api.users import UsersApi
from nessus.util import Logger


class NessusClient(object):

    MAX_RETRIES = 3
    RETRY_SLEEP_MILLISECONDS = 500

    def __init__(
            self,
            access_key=NessusConfig.get('access_key'),
            secret_key=NessusConfig.get('secret_key'),
            endpoint=NessusConfig.get('endpoint'),
    ):
        self._access_key = access_key
        self._secret_key = secret_key
        self._endpoint = endpoint

        self._headers = {
            u'X-ApiKeys': u'accessKey=%s; secretKey=%s;' % (self._access_key, self._secret_key)
        }

        self._ini_api()

    def _ini_api(self):
        """
        Initialize all api.
        """
        self.asset_lists = AssetListsApi(self)
        self.editor = EditorApi(self)
        self.exclusions = ExclusionApi(self)
        self.file = FileApi(self)
        self.folders = FoldersApi(self)
        self.groups = GroupsApi(self)
        self.policies = PoliciesApi(self)
        self.scans = ScansApi(self)
        self.session = SessionApi(self)
        self.users = UsersApi(self)

    def _retry(f):
        """
        Decorator to retry when NessusRetryableException is caught.
        :param f: Method to retry.
        :return: A decorated method that implicitly retry the original method upon NessusRetryableException is caught.
        """
        def wrapper(*args, **kwargs):
            count = 0
            retry = True
            sleep_ms = 0

            while retry:
                retry = False
                try:
                    return f(*args, **kwargs)
                except NessusRetryableException as exception:
                    count += 1

                    if count <= NessusClient.MAX_RETRIES:
                        retry = True
                        sleep_ms += count * NessusClient.RETRY_SLEEP_MILLISECONDS
                        Logger.warn(u'Retry %d of %d. Sleep %dms' % (count, NessusClient.MAX_RETRIES, sleep_ms),
                                    NessusClient)
                        sleep(sleep_ms / 1000.0)
                    else:
                        raise NessusException(exception.response)

        return wrapper

    def _error_handler(f):
        """
        Decorator to handle response error.
        :param f: Response returning method.
        :return: A Response returning method that raises NessusException for error in response.
        """
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            exception = None

            if response.status_code == 429:
                raise NessusRetryableException(response)
            if response.status_code in [501, 502, 503]:
                raise NessusRetryableException(response)
            if not 200 <= response.status_code <= 299:
                raise NessusException(response)

            return response
        return wrapper

    @_retry
    @_error_handler
    def get(self, uri, path_params=None, **kwargs):
        return self._request('GET', uri, path_params, **kwargs)

    @_retry
    @_error_handler
    def post(self, uri, payload=None, path_params=None, **kwargs):
        if isinstance(payload, BaseRequest):
            payload = payload.as_payload()
        return self._request('POST', uri, path_params, json=payload, **kwargs)

    @_retry
    @_error_handler
    def put(self, uri, payload=None, path_params=None, **kwargs):
        if isinstance(payload, BaseRequest):
            payload = payload.as_payload()
        return self._request('PUT', uri, path_params, json=payload, **kwargs)

    @_retry
    @_error_handler
    def delete(self, uri, path_params=None, **kwargs):
        return self._request('DELETE', uri, path_params, **kwargs)

    def _request(self, method, uri, path_params=None, **kwargs):
        if path_params:
            # Ensure path param is encoded.
            path_params = {key: quote(str(value), safe=u'') for key, value in path_params.items()}
            uri = uri % path_params
        return requests.request(method, self._endpoint + uri, headers=self._headers, **kwargs)

    # Delayed qualifying decorator as staticmethod. This is a workaround to error raised from using a decorator
    # decorated by @staticmethod.
    _retry = staticmethod(_retry)
    _error_handler = staticmethod(_error_handler)
