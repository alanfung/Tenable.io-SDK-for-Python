from nessus.api.base import BaseApi
from nessus.api.models import ServerProperties, ServerStatus


class ServerApi(BaseApi):

    def properties(self):
        """Return the server version and other properties.

        :raise NessusApiException:  When API error is encountered.
        :return: An instance of :class:`nessus.api.models.ServerStatus`.
        """
        response = self._client.get('server/properties')
        return ServerProperties.from_json(response.text)

    def status(self):
        """Return server status.

        :raise NessusApiException:  When API error is encountered.
        :return: An instance of :class:`nessus.api.models.ServerStatus`.
        """
        response = self._client.get('server/status')
        return ServerStatus.from_json(response.text)
