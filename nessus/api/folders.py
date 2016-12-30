from json import loads

from nessus.api.base import BaseApi
from nessus.api.models import Folder, FolderList


class FoldersApi(BaseApi):

    def create(self, name):
        """Create a new folder for the current user.

        :param name: The folder name.
        :raise NessusApiException:  When API error is encountered.
        :return: The ID of the folder created.
        """
        response = self._client.post('folders', {'name': name})
        return loads(response.text).get('id')

    def edit(self, folder_id, name):
        """Rename the folder.

        :param folder_id: The folder ID.
        :param name: The folder name to be renamed.
        :raise NessusApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.put('folders/%(folder_id)s', {'name': name}, {'folder_id': folder_id})
        return True

    def delete(self, folder_id):
        """Delete the folder.

        :param folder_id: The folder ID.
        :raise NessusApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('folders/%(folder_id)s', {'folder_id': folder_id})
        return True

    def list(self):
        """Returns the current user's scan folders.

        :raise NessusApiException:  When API error is encountered.
        :return: An instance of :class"`nessus.api.models.FolderList`.
        """
        response = self._client.get('folders')
        return FolderList.from_json(response.text)
