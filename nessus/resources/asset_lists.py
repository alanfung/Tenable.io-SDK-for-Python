from nessus.resources.base import BaseResource, BaseRequest
from nessus.resources.models import AssetList, AssetListList


class AssetListsResource(BaseResource):

    def list(self):
        response = self._client.get('asset-lists')
        return AssetListList.from_json(response.text)

    def create(self, asset_list_create):
        response = self._client.post('asset-lists', asset_list_create)
        return AssetList.from_json(response.text)

    def delete(self, asset_list_id):
        self._client.delete('asset-lists/%(list_id)s', {'list_id': asset_list_id})
        return True

    def details(self, asset_list_id):
        response = self._client.get('asset-lists/%(list_id)s', {'list_id': asset_list_id})
        return AssetList.from_json(response.text)


class AssetListCreateRequest(BaseRequest):

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
