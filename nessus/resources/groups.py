from nessus.resources.base import BaseResource
from nessus.resources.models import Group, GroupList, UserList


class GroupsResource(BaseResource):

    def add_user(self, group_id, user_id):
        self._client.post('groups/%(group_id)s/users/%(user_id)s', {}, path_params={'group_id': group_id, 'user_id': user_id})
        return True

    def create(self, name):
        response = self._client.post('groups', {'name': name})
        return Group.from_json(response.text)

    def delete(self, group_id):
        self._client.delete('groups/%(group_id)s', {'group_id': group_id})
        return True

    def delete_user(self, group_id, user_id):
        self._client.delete('groups/%(group_id)s/users/%(user_id)s', {'group_id': group_id, 'user_id': user_id})
        return True

    def edit(self, group_id, name):
        self._client.put('groups/%(group_id)s', {'name': name}, {'group_id': group_id})
        return True

    def list(self):
        response = self._client.get('groups')
        return GroupList.from_json(response.text)

    def list_users(self, group_id):
        response = self._client.get('groups/%(group_id)s/users', {'group_id': group_id})
        return UserList.from_json(response.text)
