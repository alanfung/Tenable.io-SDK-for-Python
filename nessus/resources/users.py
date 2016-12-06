import json

from nessus.resources.base import BaseResource
from nessus.resources.model import User


class UsersResource(BaseResource):

    def get(self, user_id):
        response = self._client.get('users/%(user_id)s', {'user_id': user_id})
        return User.from_json(response.text)

    def list(self):
        response = self._client.get('users')
        return json.loads(response.text)

    def impersonate(self, user_id):
        response = self._client.post('users/%(user_id)/impersonate', path_params={'user_id': user_id})
        return json.loads(response.text)
