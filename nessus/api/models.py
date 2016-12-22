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


class Exclusion(BaseModel):
    def __init__(
            self,
            id=None,
            name=None,
            description=None,
            schedule=None,
            creation_date=None,
            last_modification_date=None,
            members=None,
    ):
        self._schedule = None

        self.id = id
        self.name = name
        self.description = description
        self.schedule = schedule
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date
        self.members = members

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        if isinstance(schedule, ExclusionSchedule):
            self._schedule = schedule
        elif isinstance(schedule, dict):
            self._schedule = ExclusionSchedule.from_dict(schedule)
        else:
            self._schedule = None


class ExclusionList(BaseModel):
    def __init__(
            self,
            exclusions=None
    ):
        self._exclusions = None
        self.exclusions = exclusions

    @property
    def exclusions(self):
        return self._exclusions

    @exclusions.setter
    @BaseModel._model_list(Exclusion)
    def exclusions(self, exclusions):
        self._exclusions = exclusions


class ExclusionSchedule(BaseModel):

    def __init__(
            self,
            enabled=None,
            starttime=None,
            endtime=None,
            timezone=None,
            rrules=None
    ):
        self._rrules = None

        self.enabled = enabled
        self.starttime = starttime
        self.endtime = endtime
        self.timezone = timezone
        self.rrules = rrules

    @property
    def rrules(self):
        return self._rrules

    @rrules.setter
    def rrules(self, rrules):
        if isinstance(rrules, ExclusionRrules):
            self._rrules = rrules
        elif isinstance(rrules, dict):
            self._rrules = ExclusionRrules.from_dict(rrules)
        else:
            self._rrules = None

    def as_payload(self, filter_=None):
        payload = super(ExclusionSchedule, self).as_payload(True)
        if isinstance(self.rrules, ExclusionRrules):
            payload.__setitem__('rrules', self.rrules.as_payload(True))
        else:
            payload.pop('rrules', None)
        payload.pop('_rrules', None)
        return payload


class ExclusionRrules(BaseModel):

    def __init__(
            self,
            freq=None,
            interval=None,
            byweekday=None,
            bymonthday=None
    ):
        self.freq = freq
        self.interval = interval
        self.byweekday = byweekday
        self.bymonthday = bymonthday


class Folder(BaseModel):
    def __init__(
            self,
            id=None,
            name=None,
            type=None,
            default_tag=None,
            custom=None,
            unread_count=None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.default_tag = default_tag
        self.custom = custom
        self.unread_count = unread_count


class FolderList(BaseModel):

    def __init__(
            self,
            folders=None,
    ):
        self._folders = None

        self.folders = folders

    @property
    def folders(self):
        return self._folders

    @folders.setter
    @BaseModel._model_list(Folder)
    def folders(self, folders):
        self._folders = folders


class Group(BaseModel):

    def __init__(
            self,
            id=None,
            name=None,
            permissions=None,
            user_count=None,
    ):
        self.id = id
        self.name = name
        self.permissions = permissions
        self.user_count = user_count


class GroupList(BaseModel):

    def __init__(
            self,
            groups=None,
    ):
        self._groups = None

        self.groups = groups

    @property
    def groups(self):
        return self._groups

    @groups.setter
    @BaseModel._model_list(Group)
    def groups(self, groups):
        self._groups = groups


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


class Scan(BaseModel):

    STATUS_ABORTED = u'aborted'
    STATUS_CANCELED = u'canceled'
    STATUS_COMPLETED = u'completed'
    STATUS_EMPTY = u'empty'
    STATUS_PAUSED = u'paused'
    STATUS_PAUSING = u'pausing'
    STATUS_PENDING = u'pending'
    STATUS_RESUMING = u'resuming'
    STATUS_RUNNING = u'running'
    STATUS_STOPPING = u'stopping'

    def __init__(
            self,
            id=None,
            uuid=None,
            name=None,
            type=None,
            owner=None,
            enabled=None,
            folder_id=None,
            read=None,
            status=None,
            shared=None,
            user_permissions=None,
            creation_date=None,
            last_modification_date=None,
            control=None,
            starttime=None,
            timezone=None,
            rrules=None,
    ):
        self.id = id
        self.uuid = uuid
        self.name = name
        self.type = type
        self.owner = owner
        self.enabled = enabled
        self.folder_id = folder_id
        self.read = read
        self.status = status
        self.shared = shared
        self.user_permissions = user_permissions
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date
        self.control = control
        self.starttime = starttime
        self.timezone = timezone
        self.rrules = rrules


class ScanDetails(BaseModel):

    def __init__(
            self,
            info=None,
            hosts=None,
            comphosts=None,
            notes=None,
            remediations=None,
            vulnerabilities=None,
            compliance=None,
            history=None,
            filters=None,
    ):
        self._info = None

        self.info = info
        self.hosts = hosts
        self.comphosts = comphosts
        self.notes = notes
        self.remediations = remediations
        self.vulnerabilities = vulnerabilities
        self.compliance = compliance
        self.history = history
        self.filters = filters

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, info):
        if isinstance(info, ScanDetailsInfo):
            self._info = info
        elif isinstance(info, dict):
            self._info = ScanDetailsInfo.from_dict(info)
        else:
            self._info = None


class ScanDetailsInfo(BaseModel):

    def __init__(
            self,
            acls=None,
            edit_allowed=None,
            status=None,
            policy=None,
            pci_can_upload=None,  # API uses "pci-can-upload" which is not a valid python attribute name.
            hasaudittrail=None,
            scan_start=None,
            folder_id=None,
            targets=None,
            timestamp=None,
            object_id=None,
            scanner_name=None,
            haskb=None,
            uuid=None,
            hostcount=None,
            scan_end=None,
            name=None,
            user_permissions=None,
            control=None,
    ):
        self.acls = acls
        self.edit_allowed = edit_allowed
        self.status = status
        self.policy = policy
        self.pci_can_upload = pci_can_upload
        self.hasaudittrail = hasaudittrail
        self.scan_start = scan_start
        self.folder_id = folder_id
        self.targets = targets
        self.timestamp = timestamp
        self.object_id = object_id
        self.scanner_name = scanner_name
        self.haskb = haskb
        self.uuid = uuid
        self.hostcount = hostcount
        self.scan_end = scan_end
        self.name = name
        self.user_permissions = user_permissions
        self.control = control

    @classmethod
    def from_dict(cls, dict_):
        # Because API uses "pci-can-upload" API uses "pci-can-upload" which is not a valid python attribute name.
        if 'pci-can-upload' in dict_:
            dict_['pci_can_upload'] = dict_.pop('pci-can-upload')
        return super(ScanDetailsInfo, cls).from_dict(dict_)

    def as_payload(self, filter_=None):
        # Because API uses "pci-can-upload" API uses "pci-can-upload" which is not a valid python attribute name.
        payload = self.as_payload(filter_)
        if 'pci_can_upload' in payload:
            payload['pci-can-upload'] = payload.pop('pci_can_upload')
        return payload


class ScanList(BaseModel):

    def __init__(
            self,
            folders=None,
            scans=None,
            timestamp=None,
    ):
        self._scans = None
        self.folders = folders
        self.scans = scans
        self.timestamp = timestamp

    @property
    def scans(self):
        return self._scans

    @scans.setter
    @BaseModel._model_list(Scan)
    def scans(self, scans):
        self._scans = scans


class ScanSettings(BaseModel):

    def __init__(
            self,
            name,
            text_targets,
            description=None,
            emails=None,
            enabled=True,
            launch=None,
            folder_id=None,
            policy_id=None,
            scanner_id=None,
    ):
        self.name = name
        self.description = description
        self.emails = emails
        self.enabled = enabled
        self.launch = launch
        self.folder_id = folder_id
        self.policy_id = policy_id
        self.scanner_id = scanner_id
        self.text_targets = text_targets


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


class UserKeys(BaseModel):

    def __init__(
            self,
            access_key=None,
            secret_key=None,
    ):
        self.access_key = access_key
        self.secret_key = secret_key

    @classmethod
    def from_dict(cls, dict_):
        # Because API uses camelCase for some reason; normalize to underscore here.
        if 'accessKey' in dict_:
            dict_['access_key'] = dict_.pop('accessKey')
        if 'secretKey' in dict_:
            dict_['secret_key'] = dict_.pop('secretKey')
        return super(UserKeys, cls).from_dict(dict_)

    def as_payload(self, filter_=None):
        # Because API uses camelCase for some reason; normalize to underscore here.
        payload = self.as_payload(filter_)
        if 'access_key' in payload:
            payload['accessKey'] = payload.pop('access_key')
        if 'secret_key' in payload:
            payload['secretKey'] = payload.pop('secret_key')
        return payload


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
