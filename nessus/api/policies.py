from nessus.api.base import BaseApi
from nessus.api.models import PolicyList


class PoliciesApi(BaseApi):

    def list(self):
        response = self._client.get('policies')
        return PolicyList.from_json(response.text)
