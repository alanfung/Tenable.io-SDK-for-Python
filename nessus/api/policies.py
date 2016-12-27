from nessus.api.base import BaseApi
from nessus.api.models import PolicyList


class PoliciesApi(BaseApi):

    def list(self):
        """Return the policy list.

        :raise NessusApiException:  When API error is encountered.
        :return: An instance of :class:`nessus.api.models.PolicyList`.
        """
        response = self._client.get('policies')
        return PolicyList.from_json(response.text)
