from json import loads

from nessus.resources.base import BaseResource
from nessus.resources.models import ScanDetails, ScanList, ScanSettings
from nessus.resources.base import BaseRequest


class ScansResource(BaseResource):

    def create(self, scan_create):
        response = self._client.post('scans', scan_create)
        return loads(response.text).get('scan', {}).get('id')

    def delete(self, scan_id):
        self._client.delete('scans/%(scan_id)s', path_params={'scan_id': scan_id})
        return True

    def details(self, scan_id):
        response = self._client.get('scans/%(scan_id)s', path_params={'scan_id': scan_id})
        return ScanDetails.from_json(response.text)

    def launch(self, scan_id):
        """
        :return: scan_uuid
        """
        response = self._client.post('scans/%(scan_id)s/launch', {}, path_params={'scan_id': scan_id})
        return loads(response.text).get('scan_uuid')

    def list(self):
        response = self._client.get('scans')
        return ScanList.from_json(response.text)

    def pause(self, scan_id):
        self._client.post('scans/%(scan_id)s/pause', {}, path_params={'scan_id': scan_id})
        return True

    def resume(self, scan_id):
        self._client.post('scans/%(scan_id)s/resume', {}, path_params={'scan_id': scan_id})
        return True

    def stop(self, scan_id):
        self._client.post('scans/%(scan_id)s/stop', {}, path_params={'scan_id': scan_id})
        return True


class ScanCreateRequest(BaseRequest):

    def __init__(
            self,
            uuid,
            settings,
    ):
        assert isinstance(settings, ScanSettings)
        self.uuid = uuid
        self.settings = settings

    def as_payload(self, filter_=None):
        return {
            'uuid': self.uuid,
            'settings': self.settings.as_payload(True)
        }
