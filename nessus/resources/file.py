from json import loads

from nessus.resources.base import BaseResource


class FileResource(BaseResource):

    def upload(self, file):
        response = self._client.post('file/upload', files={'Filedata': (file.name, file)})
        return loads(response.text).get('fileuploaded')
