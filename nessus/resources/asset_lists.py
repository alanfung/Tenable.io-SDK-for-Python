import json

from nessus.resources.base import BaseResource
from nessus.resources.model import AssetList


class AssetListsResource(BaseResource):

    def list(self):
        response = self._client.get('asset-lists')
        return AssetList.from_list(json.loads(response.text)['asset_lists'])

    def create(self, asset_list_create):
        response = self._client.post('asset-lists', asset_list_create.__dict__)
        return AssetList.from_json(response.text)


class AssetListCreateRequest(object):

    def __init__(
            self,
            name=None,
            members=None,
            type=None,
            acls=None
    ):
        self.name = name
        self.members = members
        self.type = type
        self.acls = acls
