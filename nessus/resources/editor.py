from nessus.resources.base import BaseResource
from nessus.resources.models import TemplateList


class EditorResource(BaseResource):

    def list(self, type):
        response = self._client.get('editor/%(type)s/templates', path_params={'type': type})
        return TemplateList.from_json(response.text)
