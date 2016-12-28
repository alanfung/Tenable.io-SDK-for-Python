from nessus.api.models import ServerProperties, ServerStatus
from tests.base import BaseTest


class TestServerApi(BaseTest):

    def test_server_properties(self, client):
        server_properties = client.server.properties()

        assert isinstance(server_properties, ServerProperties), u'The `property` method return type.'

    def test_server_status(self, client):
        server_status = client.server.status()

        assert isinstance(server_status, ServerStatus), u'The `status` method return type.'
