from nessus.api.base import BaseApi
from nessus.api.models import Session


class SessionApi(BaseApi):

    def get(self):
        response = self._client.get('session')
        return Session.from_json(response.text)
