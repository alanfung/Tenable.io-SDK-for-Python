from json import loads

from nessus.resources.base import BaseResource, BaseRequest
from nessus.resources.models import User, UserList


class UsersResource(BaseResource):

    def get(self, user_id):
        response = self._client.get('users/%(user_id)s', {'user_id': user_id})
        return User.from_json(response.text)

    def list(self):
        response = self._client.get('users')
        return UserList.from_json(response.text)

    def impersonate(self, user_id):
        response = self._client.post('users/%(user_id)s/impersonate', path_params={'user_id': user_id})
        return loads(response.text)

    def create(self, user_create):
        response = self._client.post('users', user_create)
        return loads(response.text).get('id')

    def edit(self, user_id, user_edit):
        response = self._client.put('users/%(user_id)s', user_edit, {'user_id': user_id})
        return User.from_json(response.text)

    def delete(self, user_id):
        self._client.delete('users/%(user_id)s', {'user_id': user_id})
        return True

    def password(self, user_id, password):
        self._client.put('users/%(user_id)s/chpasswd', {'password': password}, {'user_id': user_id})
        return True


class UserCreateRequest(BaseRequest):

    def __init__(
            self,
            username=None,
            password=None,
            permissions=None,
            name=None,
            email=None,
            type=None
    ):
        self.username = username
        self.password = password
        self.permissions = permissions
        self.name = name
        self.email = email
        self.type = type


class UserEditRequest(BaseRequest):

    def __init__(
            self,
            permissions=None,
            name=None,
            email=None
    ):
        self.permissions = permissions
        self.name = name
        self.email = email
