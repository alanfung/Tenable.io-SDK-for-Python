import os

from json import loads

from nessus.api.base import BaseApi


class FileApi(BaseApi):

    def upload(self, file):
        """Upload a file

        :param file: An instance of file object
        :raise NessusApiException:  When API error is encountered.
        :return: The name of the uploaded file.
        """
        response = self._client.post('file/upload', files={'Filedata': (os.path.basename(file.name), file)})
        return loads(response.text).get('fileuploaded')
