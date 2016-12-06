from nessus.resources.base import BaseResource
from nessus.resources.models import Session


class SessionResource(BaseResource):

    def get(self):
        response = self._client.get('session')
        return Session.from_json(response.text)
