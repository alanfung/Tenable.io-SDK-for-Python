from nessus.api.base import BaseApi
from nessus.api.models import TemplateList


class EditorApi(BaseApi):

    def list(self, type):
        response = self._client.get('editor/%(type)s/templates', path_params={'type': type})
        return TemplateList.from_json(response.text)
