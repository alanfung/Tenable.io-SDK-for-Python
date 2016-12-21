from nessus.api.base import BaseApi, BaseRequest
from nessus.api.models import Exclusion, ExclusionList, ExclusionSchedule


class ExclusionApi(BaseApi):

    def create(self, exclusion_create):
        response = self._client.post('exclusions', exclusion_create)
        return Exclusion.from_json(response.text)

    def delete(self, list_id):
        self._client.delete('exclusions/%(list_id)s', path_params={'list_id': list_id})
        return True

    def details(self, list_id):
        response = self._client.get('exclusions/%(list_id)s', path_params={'list_id': list_id})
        return Exclusion.from_json(response.text)

    def edit(self, list_id, exclusion_edit):
        response = self._client.put('exclusions/%(list_id)s', exclusion_edit, path_params={'list_id': list_id})
        return Exclusion.from_json(response.text)

    def list(self):
        response = self._client.get('exclusions')
        return ExclusionList.from_json(response.text)


class ExclusionSaveBaseRequest(BaseRequest):

    def __init__(
            self,
            name,
            members=None,
            description=None,
            schedule=None
    ):
        self.name = name
        self.members = members
        self.description = description
        self.schedule = schedule

    def as_payload(self, filter_=None):
        payload = super(ExclusionSaveBaseRequest, self).as_payload(True)
        if isinstance(self.schedule, ExclusionSchedule):
            payload.__setitem__('schedule', self.schedule.as_payload())
        else:
            payload.pop('schedule', None)
        return payload


class ExclusionCreateRequest(ExclusionSaveBaseRequest):

    def __init__(
            self,
            name,
            members,
            description=None,
            schedule=None
    ):
        super(ExclusionCreateRequest, self).__init__(name, members, description, schedule)


class ExclusionEditRequest(ExclusionSaveBaseRequest):

    def __init__(
            self,
            name=None,
            members=None,
            description=None,
            schedule=None
    ):
        super(ExclusionEditRequest, self).__init__(name, members, description, schedule)

