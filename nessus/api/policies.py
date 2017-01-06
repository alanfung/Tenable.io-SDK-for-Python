from json import loads

from nessus.api.base import BaseApi
from nessus.api.models import PolicyDetails, PolicySettings, PolicyList
from nessus.api.base import BaseRequest


class PoliciesApi(BaseApi):

    def configure(self, policy_id, policy_configure_request):
        """Update a policy.

        :param policy_id: Policy id.
        :param policy_configure_request: An instance of :class:`PolicyConfigureRequest`.
        :raise NessusApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.put('policies/%(policy_id)s', policy_configure_request,
                         path_params={'policy_id': policy_id})
        return True

    def create(self, policy_create_request):
        """Create a policy.

        :param policy_create_request: An instance of :class:`PolicyCreateRequest`.
        :raise NessusApiException:  When API error is encountered.
        :return: Policy id.
        """
        response = self._client.post('policies', policy_create_request)
        return loads(response.text).get('policy_id')

    def copy(self, policy_id):
        """Copy a policy.

        :param policy_id: Policy id.
        :raise NessusApiException:  When API error is encountered.
        :return: Policy id.
        """
        response = self._client.post('policies/%(policy_id)s/copy', {},
                                     path_params={'policy_id': policy_id})
        return loads(response.text).get('id')

    def delete(self, policy_id):
        """Delete a policy.

        :param policy_id: Policy id.
        :raise NessusApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('policies/%(policy_id)s',
                            path_params={'policy_id': policy_id})
        return True

    def details(self, policy_id):
        """Get policy details.

        :param policy_id: Policy id.
        :raise NessusApiException:  When API error is encountered.
        :return: An instance of :class:`PolicyDetails`.
        """
        response = self._client.get('policies/%(policy_id)s',
                                    path_params={'policy_id': policy_id})
        return PolicyDetails.from_json(response.text)

    def import_policy(self, policy_import_request):
        """Import a policy.

        :param policy_import_request: An instance of :class:`PolicyImportRequest`.
        :raise NessusApiException:  When API error is encountered.
        :return: Policy id.
        """
        response = self._client.post('policies/import', policy_import_request)
        return loads(response.text).get('id')

    def export(self, policy_id, stream=True, chunk_size=1024):
        """Export a policy.

        :param policy_id: Policy id.
        :param stream: Defaults to True. If False, the response content will be immediately downloaded.
        :param chunk_size: If Stream=False, data is returned as a single chunk.
        :raise NessusApiException:  When API error is encountered.
        :return: Response content iterator.
        """
        response = self._client.get('policies/%(policy_id)s/export',
                                    path_params={'policy_id': policy_id},
                                    stream=stream)
        return response.iter_content(chunk_size=chunk_size)

    def list(self):
        """Return the policy list.

        :raise NessusApiException:  When API error is encountered.
        :return: An instance of :class:`nessus.api.models.PolicyList`.
        """
        response = self._client.get('policies')
        return PolicyList.from_json(response.text)


class PolicyCreateRequest(BaseRequest):

    def __init__(
            self,
            uuid,
            settings,
            ):
        assert isinstance(settings, PolicySettings)
        self.uuid = uuid
        self.settings = settings

    def as_payload(self, filter_=None):
        return {
            'uuid': self.uuid,
            'settings': self.settings.as_payload(True)
        }


class PolicyConfigureRequest(PolicyCreateRequest):
    pass


class PolicyImportRequest(BaseRequest):

    def __init__(
        self,
        file,
    ):
        self.file = file
