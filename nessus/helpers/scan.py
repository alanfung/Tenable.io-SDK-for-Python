from time import sleep, time

from nessus.api.models import Scan, ScanSettings, Template
from nessus.api.scans import ScansApi, ScanCreateRequest, ScanExportRequest
from nessus.exceptions import NessusException


class ScanHelper(object):

    def __init__(self, client):
        self._client = client

    def id(self, id):
        """
        Get scan by ID.
        :param id: Scan ID.
        :return: ScanRef referenced by id if exists.
        """
        scan_detail = self._client.scans.details(id)
        return ScanRef(self._client, scan_detail.info.object_id)

    def create(self, name, text_targets, template):
        """
        Get scan by ID.
        :param name: The name of the Scan to be created.
        :param text_targets: A list of scan targets separated by commas.
        :param template: The name or title of the template, or an instance of Template.
        :return: ScanRef referenced by id if exists.
        """
        t = template

        if not isinstance(t, Template):
            t = self.template(name=template)

        if not t:
            t = self.template(title=template)

        if not t:
            raise NessusException(u'Template with name or title as "%s" not found.' % template)

        scan_id = self._client.scans.create(
            ScanCreateRequest(
                t.uuid,
                ScanSettings(
                    name,
                    text_targets,
                )
            )
        )
        return ScanRef(self._client, scan_id)

    def template(self, name=None, title=None):
        """
        Get template by name or title. The `title` argument is ignored if `name` is passed.
        :param name: The name of the template.
        :param title: The title of the template.
        :return: An instance of Template if exists, otherwise None.
        """
        template = None

        if name:
            template_list = self._client.editor.list('scan')
            for t in template_list.templates:
                if t.name == name:
                    template = t
                    break

        elif title:
            template_list = self._client.editor.list('scan')
            for t in template_list.templates:
                if t.title == title:
                    template = t
                    break

        return template


class ScanRef(object):

    STATUSES_STOPPED = [
        Scan.STATUS_ABORTED,
        Scan.STATUS_CANCELED,
        Scan.STATUS_COMPLETED,
    ]

    def __init__(self, client, id):
        self._client = client
        self.id = id

    def delete(self):
        self._client.scans.delete(self.id)
        return self

    def details(self):
        return self._client.scans.details(self.id)

    def download(self, path, format=ScanExportRequest.FORMAT_PDF, file_open_mode='wb'):
        self.wait_until_stopped()

        file_id = self._client.scans.export_request(
            self.id,
            ScanExportRequest(format=format)
        )
        self._wait_until(
            lambda: self._client.scans.export_status(self.id, file_id) == ScansApi.STATUS_EXPORT_READY)

        iter_content = self._client.scans.export_download(self.id, file_id)
        with open(path, file_open_mode) as fd:
            for chunk in iter_content:
                fd.write(chunk)
        return self

    def launch(self):
        self._client.scans.launch(self.id)
        return self

    @property
    def status(self):
        return self.details().info.status

    def stop(self):
        self._client.scans.stop(self.id)
        self.wait_until_stopped()
        return self

    def wait_or_cancel_after(self, seconds):
        start_time = time()
        self._wait_until(lambda: time() - start_time > seconds or self.status in ScanRef.STATUSES_STOPPED)
        if self.status not in ScanRef.STATUSES_STOPPED:
            self.stop()
        return self

    def wait_until_stopped(self):
        self._wait_until(lambda: self.status in ScanRef.STATUSES_STOPPED)
        return self

    @staticmethod
    def _wait_until(condition):
        while True:
            if condition():
                return True
            sleep(1)
