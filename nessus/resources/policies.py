from nessus.resources.base import BaseResource
from nessus.resources.models import PolicyList


class PoliciesResource(BaseResource):

    def list(self):
        response = self._client.get('policies')
        return PolicyList.from_json(response.text)
