from nessus.client import NessusClient
from nessus.resources.models import UserList


class TestUsersResource(object):

    def test_list_return_correct_type(self):
        user_list = NessusClient().users.list()
        assert isinstance(user_list, UserList), u'The `list` method returns type.'

    def test_get_return_correct_user(self):
        user_list = NessusClient().users.list()

        assert len(user_list.users) > 0, u'User list has at least one user for testing.'

        user = user_list.users[0]

        assert hasattr(user, 'id'), u'User has ID.'

        got_user = NessusClient().users.get(user.id)

        assert got_user.id == user.id, u'The `get` method returns user with the same ID.'
        assert got_user.email == user.email, u'The `get` method returns user with the same email.'
        assert got_user.username == user.username, u'The `get` method returns user with the same username.'
