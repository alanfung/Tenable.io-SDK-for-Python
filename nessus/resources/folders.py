from json import loads

from nessus.resources.base import BaseResource
from nessus.resources.models import Folder, FolderList


class FoldersResource(BaseResource):

    def create(self, name):
        response = self._client.post('folders', {'name': name})
        return loads(response.text).get('id')

    def edit(self, folder_id, name):
        self._client.put('folders/%(folder_id)s', {'name': name}, {'folder_id': folder_id})
        return True

    def delete(self, folder_id):
        self._client.delete('folders/%(folder_id)s', {'folder_id': folder_id})
        return True

    def list(self):
        response = self._client.get('folders')
        return FolderList.from_json(response.text)
