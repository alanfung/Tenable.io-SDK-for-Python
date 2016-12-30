from nessus.api.base import BaseApi
from nessus.api.models import TemplateList


class EditorApi(BaseApi):

    def list(self, type):
        """Returns the template list.

        :param type: The type of template (scan or policy).
        :raise NessusApiException:  When API error is encountered.
        :return: An instance of :class:`nessus.api.models.TemplateList`.
        """
        response = self._client.get('editor/%(type)s/templates', path_params={'type': type})
        return TemplateList.from_json(response.text)
