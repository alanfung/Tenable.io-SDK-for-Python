from json import loads

from nessus.api.base import BaseApi
from nessus.api.models import ScanDetails, ScanList, ScanSettings
from nessus.api.base import BaseRequest


class ScansApi(BaseApi):

    STATUS_EXPORT_READY = u'ready'

    def create(self, scan_create):
        response = self._client.post('scans', scan_create)
        return loads(response.text).get('scan', {}).get('id')

    def delete(self, scan_id):
        self._client.delete('scans/%(scan_id)s', path_params={'scan_id': scan_id})
        return True

    def details(self, scan_id):
        response = self._client.get('scans/%(scan_id)s', path_params={'scan_id': scan_id})
        return ScanDetails.from_json(response.text)

    def export_download(self, scan_id, file_id, stream=True, chunk_size=1024):
        response = self._client.get('scans/%(scan_id)s/export/%(file_id)s/download',
                                    path_params={'scan_id': scan_id, 'file_id': file_id},
                                    stream=stream)
        return response.iter_content(chunk_size=chunk_size)

    def export_request(self, scan_id, scan_export, history_id=None):
        """
        :return: file_id
        """
        assert isinstance(scan_export, ScanExportRequest)
        response = self._client.post('scans/%(scan_id)s/export',
                                     scan_export,
                                     path_params={'scan_id': scan_id},
                                     params={'history_id': history_id} if history_id else None)
        return loads(response.text).get('file')

    def export_status(self, scan_id, file_id):
        response = self._client.get('scans/%(scan_id)s/export/%(file_id)s/status',
                                    path_params={'scan_id': scan_id, 'file_id': file_id})
        return loads(response.text).get('status')

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


class ScanExportRequest(BaseRequest):

    FORMAT_CSV = u'csv'
    FORMAT_DB = u'db'
    FORMAT_HTML = u'html'
    FORMAT_NESSUS = u'nessus'
    FORMAT_PDF = u'pdf'

    def __init__(
            self,
            format,
            password=None,
            chapters=None,
    ):
        assert format in [
            ScanExportRequest.FORMAT_CSV,
            ScanExportRequest.FORMAT_DB,
            ScanExportRequest.FORMAT_HTML,
            ScanExportRequest.FORMAT_NESSUS,
            ScanExportRequest.FORMAT_PDF,
        ]
        self.format = format
        self.password = password
        self.chapters = chapters

    def as_payload(self, filter_=None):
        return super(ScanExportRequest, self).as_payload(True)
