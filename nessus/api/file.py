from json import loads

from nessus.api.base import BaseApi


class FileApi(BaseApi):

    def upload(self, file):
        response = self._client.post('file/upload', files={'Filedata': (file.name, file)})
        return loads(response.text).get('fileuploaded')
