from nessus.resources.base import BaseResource


class ScansResource(BaseResource):

    def list(self):
        response = self._client.get('scans')
        return response.text
