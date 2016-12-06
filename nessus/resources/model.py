from json import loads


class BaseModel(object):

    @classmethod
    def from_json(cls, json):
        return cls.from_dict(loads(json))

    @classmethod
    def from_dict(cls, dict):
        instance = cls()
        for key in dict:
            setattr(instance, key, dict[key])
        return instance

    @classmethod
    def from_list(cls, list):
        model_list = None
        if list:
            model_list = []
            for item in list:
                model_list.append(cls.from_dict(item))
        return model_list

    @classmethod
    def from_json_list(cls, json_list):
        return cls.from_list(loads(json_list))


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
