from nessus.api.base import BaseApi
from nessus.api.models import Session


class SessionApi(BaseApi):

    def get(self):
        """Return the user session data.

        :raise NessusApiException:  When API error is encountered.
        :return: An instance of :class:`nessus.api.models.Session`.
        """
        response = self._client.get('session')
        return Session.from_json(response.text)
