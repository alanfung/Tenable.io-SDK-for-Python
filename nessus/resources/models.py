from json import loads

from nessus.exceptions import NessusException
from nessus.util import payload_filter


class BaseModel(object):

    @classmethod
    def from_json(cls, json):
        return cls.from_dict(loads(json))

    @classmethod
    def from_dict(cls, dict_):
        instance = cls()
        for key in dict_:
            setattr(instance, key, dict_[key])
        return instance

    @classmethod
    def from_list(cls, list_):
        model_list = None
        if list_:
            model_list = []
            for item in list_:
                model_list.append(cls.from_dict(item))
        return model_list

    @classmethod
    def from_json_list(cls, json_list):
        return cls.from_list(loads(json_list))

    @staticmethod
    def _model_list(class_):
        """
        :param class_: The class that elements should be an instance of.
        :return: A decorator that ensures the assigning value is a list of `class_` instances.
        """
        assert issubclass(class_, BaseModel)

        def decorator(f):
            def wrapper(self, list_):
                if isinstance(list_, list):
                    model_list = []
                    for item in list_:
                        if isinstance(item, class_):
                            model_list.append(item)
                        elif isinstance(item, dict):
                            model_list.append(class_.from_dict(item))
                        else:
                            raise NessusException(u'Invalid element type.')
                    f(self, model_list)
                else:
                    f(self, [])
            return wrapper
        return decorator

    def as_payload(self, filter_=None):
        return payload_filter(self.__dict__, filter_)


class AssetList(BaseModel):

    def __init__(
        self,
        id=None,
        default_list=None,
        name=None,
        members=None,
        type=None,
        owner=None,
        owner_id=None,
        last_modification_date=None,
        shared=None,
        user_permissions=None,
    ):
        self.id = id
        self.default_list = default_list
        self.name = name
        self.members = members
        self.type = type
        self.owner = owner
        self.owner_id = owner_id
        self.last_modification_date = last_modification_date
        self.shared = shared
        self.user_permissions = user_permissions


class AssetListList(BaseModel):

    def __init__(
            self,
            asset_lists=None,
    ):
        self._asset_lists = None
        self.asset_lists = asset_lists

    @property
    def asset_lists(self):
        return self._asset_lists

    @asset_lists.setter
    @BaseModel._model_list(AssetList)
    def asset_lists(self, asset_lists):
        self._asset_lists = asset_lists
    
    
class Policy(BaseModel):
    
    def __init__(
            self,
            id=None,
            template_uuid=None,
            name=None,
            description=None,
            owner_id=None,
            owner=None,
            shared=None,
            user_permissions=None,
            creation_date=None,
            last_modification_date=None,
            visibility=None,
            no_target=None,
    ):
        self.id = id
        self.template_uuid = template_uuid
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.owner = owner
        self.shared = shared
        self.user_permissions = user_permissions
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date
        self.visibility = visibility
        self.no_target = no_target


class PolicyList(BaseModel):

    def __init__(
            self,
            policies=None,
    ):
        self._policies = None

        self.policies = policies

    @property
    def policies(self):
        return self._policies

    @policies.setter
    @BaseModel._model_list(Policy)
    def policies(self, policies):
        self._policies = policies


class Session(BaseModel):

    def __init__(
            self,
            id=None,
            username=None,
            email=None,
            name=None,
            type=None,
            permissions=None,
            lastlogin=None,
            container_id=None,
            groups=None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.name = name
        self.type = type
        self.permissions = permissions
        self.lastlogin = lastlogin
        self.container_id = container_id
        self.groups = groups


class Template(BaseModel):

    def __init__(
            self,
            uuid=None,
            name=None,
            title=None,
            description=None,
            cloud_only=None,
            subscription_only=None,
            is_agent=None,
            more_info=None,
    ):
        self.uuid = uuid
        self.name = name
        self.title = title
        self.description = description
        self.cloud_only = cloud_only
        self.subscription_only = subscription_only
        self.is_agent = is_agent
        self.more_info = more_info


class TemplateList(BaseModel):

    def __init__(
            self,
            templates=None,
    ):
        self._templates = templates

        self.templates = templates

    @property
    def templates(self):
        return self._templates

    @templates.setter
    @BaseModel._model_list(Template)
    def templates(self, templates):
        self._templates = templates


class User(BaseModel):

    def __init__(
            self,
            id=None,
            username=None,
            name=None,
            email=None,
            permissions=None,
            lastlogin=None,
            type=None,
            login_fail_count=None,
            last_login_attempt=None,
    ):
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self.permissions = permissions
        self.lastlogin = lastlogin
        self.type = type
        self.login_fail_count = login_fail_count
        self.last_login_attempt = last_login_attempt


class UserList(BaseModel):

    def __init__(
            self,
            users=None,
    ):
        self._users = None
        self.users = users

    @property
    def users(self):
        return self._users

    @users.setter
    @BaseModel._model_list(User)
    def users(self, users):
        self._users = users
