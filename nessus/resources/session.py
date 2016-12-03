from nessus.resources.base import BaseResource
from nessus.resources.model import Session


class SessionResource(BaseResource):

    def get(self):
        response = self._client.get('session')
        return Session().from_json(response.text)
