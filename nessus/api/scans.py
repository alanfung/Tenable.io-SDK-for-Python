from json import loads

from nessus.api.base import BaseApi
from nessus.api.models import Scan, ScanDetails, ScanList, ScanSettings
from nessus.api.base import BaseRequest


class ScansApi(BaseApi):

    STATUS_EXPORT_READY = u'ready'

    def configure(self, scan_id, scan_configure):
        """Configure an existing scan.

        :param scan_id:
        :param scan_configure: An instance of :class:`ScanConfigureRequest`.
        :raise NessusApiException:  When API error is encountered.
        :return: The ID of scan just configured.
        """
        response = self._client.put('scans/%(scan_id)s', scan_configure, path_params={'scan_id': scan_id})
        return loads(response.text).get('scan', {}).get('id')

    def create(self, scan_create):
        """Create a scan.

        :param scan_create: An instance of :class:`ScanCreateRequest`.
        :raise NessusApiException:  When API error is encountered.
        :return: The ID of scan just created.
        """
        response = self._client.post('scans', scan_create)
        return loads(response.text).get('scan', {}).get('id')

    def copy(self, scan_id):
        response = self._client.post('scans/%(scan_id)s/copy',
                                     {},
                                     path_params={'scan_id': scan_id})
        return Scan.from_json(response.text)

    def delete(self, scan_id):
        """Delete a scan. NOTE: Scans in running, paused or stopping states can not be deleted.

        :raise NessusApiException:  When API error is encountered.
        :param scan_id: The scan ID.
        :return: True if successful.
        """
        self._client.delete('scans/%(scan_id)s', path_params={'scan_id': scan_id})
        return True

    def details(self, scan_id, history_id=None):
        """Return details of the given scan.

        :param scan_id: The scan ID.
        :param history_id: The historical data ID.
        :raise NessusApiException:  When API error is encountered.
        :return: An instance of :class:`nessus.api.models.ScanDetails`.
        """
        response = self._client.get('scans/%(scan_id)s',
                                    path_params={'scan_id': scan_id},
                                    params={'history_id': history_id} if history_id else None)

        return ScanDetails.from_json(response.text)

    def export_download(self, scan_id, file_id, stream=True, chunk_size=1024):
        """Download an exported scan.

        :param scan_id: The scan ID.
        :param file_id: The file ID.
        :param stream: Default to True. If False, the response content will be immediately downloaded.
        :param chunk_size: If Stream=False, data is returned as a single chunk.\
         If Stream=True, it's the number of bytes it should read into memory.
        :raise NessusApiException:  When API error is encountered.
        :return: The downloaded file.
        """
        response = self._client.get('scans/%(scan_id)s/export/%(file_id)s/download',
                                    path_params={'scan_id': scan_id, 'file_id': file_id},
                                    stream=stream)
        return response.iter_content(chunk_size=chunk_size)

    def export_request(self, scan_id, scan_export, history_id=None):
        """Export the given scan. Once requested, the file can be downloaded using the export\
         download method upon receiving a "ready" status from the export status method.

        :param scan_id: The scan ID.
        :param scan_export: An instance of :class:`ScanExportRequest`.
        :param history_id: The history ID of historical data.
        :raise NessusApiException:  When API error is encountered.
        :return: The file ID.
        """
        assert isinstance(scan_export, ScanExportRequest)
        response = self._client.post('scans/%(scan_id)s/export',
                                     scan_export,
                                     path_params={'scan_id': scan_id},
                                     params={'history_id': history_id} if history_id else None)
        return loads(response.text).get('file')

    def export_status(self, scan_id, file_id):
        """Check the file status of an exported scan. When an export has been requested,\
         it is necessary to poll this endpoint until a "ready" status is returned,\
          at which point the file is complete and can be downloaded using the export download endpoint.

        :param scan_id: The scan ID.
        :param file_id: The file ID.
        :raise NessusApiException:  When API error is encountered.
        :return: The file status.
        """
        response = self._client.get('scans/%(scan_id)s/export/%(file_id)s/status',
                                    path_params={'scan_id': scan_id, 'file_id': file_id})
        return loads(response.text).get('status')

    def folder(self, scan_id, folder_id):
        """Move to a scan to a folder.

        :param scan_id: The scan ID.
        :param folder_id: The folder ID.
        :raise NessusApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.put('scans/%(scan_id)s/folder',
                         {'folder_id': folder_id},
                         path_params={'scan_id': scan_id})
        return True

    def import_scan(self, scan_import):
        """Import an existing scan which has been uploaded using :func:`Nessus.FileApi.upload`

        :param scan_import: An instance of :class:`ScanImportRequest`.
        :raise NessusApiException:  When API error is encountered.
        :return: The ID of the imported scan.
        """
        response = self._client.post('scans/import', scan_import)
        return loads(response.text).get('scan', {}).get('id')

    def launch(self, scan_id):
        """Launch a scan.

        :param scan_id: The scan ID.
        :raise NessusApiException:  When API error is encountered.
        :return: The scan uuid.
        """
        response = self._client.post('scans/%(scan_id)s/launch', {}, path_params={'scan_id': scan_id})
        return loads(response.text).get('scan_uuid')

    def list(self, folder_id=None):
        """Return the scan list.

        :raise NessusApiException:  When API error is encountered.
        :return: An instance of :class:`nessus.api.models.ScanList`.
        """
        response = self._client.get('scans', params={'folder_id': folder_id} if folder_id else {})
        return ScanList.from_json(response.text)

    def pause(self, scan_id):
        """Pause a scan.

        :param scan_id: The scan ID.
        :raise NessusApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('scans/%(scan_id)s/pause', {}, path_params={'scan_id': scan_id})
        return True

    def resume(self, scan_id):
        """Resume a scan.

        :param scan_id: The scan ID.
        :raise NessusApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('scans/%(scan_id)s/resume', {}, path_params={'scan_id': scan_id})
        return True

    def stop(self, scan_id):
        """Stop a scan.

        :param scan_id: The scan ID.
        :raise NessusApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.post('scans/%(scan_id)s/stop', {}, path_params={'scan_id': scan_id})
        return True


class ScanSaveRequest(BaseRequest):

    def __init__(
            self,
            uuid,
            settings,
    ):
        assert isinstance(settings, ScanSettings)
        self.uuid = uuid
        self.settings = settings

    def as_payload(self, filter_=None):
        payload = super(ScanSaveRequest, self).as_payload(True)
        if isinstance(self.settings, ScanSettings):
            payload.__setitem__('settings', self.settings.as_payload())
        else:
            payload.pop('settings', None)
        return payload


class ScanCreateRequest(ScanSaveRequest):

    def __init__(
            self,
            uuid,
            settings=None,
    ):
        super(ScanCreateRequest, self).__init__(uuid, settings)


class ScanConfigureRequest(ScanSaveRequest):

    def __init__(
            self,
            uuid=None,
            settings=None,
    ):
        super(ScanConfigureRequest, self).__init__(uuid, settings)


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


class ScanImportRequest(BaseRequest):

    def __init__(
            self,
            file,
            folder_id=None,
            password=None
    ):
        self.file = file
        self.folder_id = folder_id
        self.password = password
