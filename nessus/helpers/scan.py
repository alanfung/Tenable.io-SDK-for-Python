import re
import time

from datetime import datetime

from nessus.api.models import Scan, ScanSettings, Template
from nessus.api.scans import ScansApi, ScanCreateRequest, ScanExportRequest
from nessus.exceptions import NessusException


class ScanHelper(object):

    def __init__(self, client):
        self._client = client

    def scans(self, name_regex=None, name=None):
        scans = self._client.scans.list().scans
        if name_regex:
            name_regex = re.compile(name_regex)
            scans = [scan for scan in scans if name_regex.match(scan.name)]
        elif name:
            scans = [scan for scan in scans if name == scan.name]
        return [ScanRef(self._client, scan.id) for scan in scans]

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

    def copy(self):
        scan = self._client.scans.copy(self.id)
        return ScanRef(self._client, scan.id)

    def delete(self):
        self._client.scans.delete(self.id)
        return self

    def details(self, history_id=None):
        return self._client.scans.details(self.id, history_id=history_id)

    def download(self, path, history_id=None, format=ScanExportRequest.FORMAT_PDF, file_open_mode='wb'):
        self.wait_until_stopped(history_id=history_id)

        file_id = self._client.scans.export_request(
            self.id,
            ScanExportRequest(format=format),
            history_id
        )
        self._wait_until(
            lambda: self._client.scans.export_status(self.id, file_id) == ScansApi.STATUS_EXPORT_READY)

        iter_content = self._client.scans.export_download(self.id, file_id)
        with open(path, file_open_mode) as fd:
            for chunk in iter_content:
                fd.write(chunk)
        return self

    def histories(self, since=None):
        histories = self.details().history
        if since:
            assert isinstance(since, datetime), '`since` parameter should be an instance of datetime.'
            ts = time.mktime(since.timetuple())
            histories = [h for h in histories if h.creation_date >= ts]
        return histories

    def launch(self, wait=True):
        self._client.scans.launch(self.id)
        if wait:
            self._wait_until(lambda: self.status() not in Scan.STATUS_PENDING)
        return self

    def pause(self, wait=True):
        self._client.scans.pause(self.id)
        if wait:
            self._wait_until(lambda: self.status() not in Scan.STATUS_PAUSING)
        return self

    def resume(self, wait=True):
        self._client.scans.resume(self.id)
        if wait:
            self._wait_until(lambda: self.status() not in Scan.STATUS_RESUMING)
        return self

    def status(self, history_id=None):
        return self.details(history_id=history_id).info.status

    def stop(self):
        self._client.scans.stop(self.id)
        self.wait_until_stopped()
        return self

    def wait_or_cancel_after(self, seconds):
        start_time = time.time()
        self._wait_until(lambda: time.time() - start_time > seconds or self.status() in ScanRef.STATUSES_STOPPED)
        if self.status() not in ScanRef.STATUSES_STOPPED:
            self.stop()
        return self

    def wait_until_stopped(self, history_id=None):
        self._wait_until(lambda: self.status(history_id=history_id) in ScanRef.STATUSES_STOPPED)
        return self

    @staticmethod
    def _wait_until(condition):
        while True:
            if condition():
                return True
            time.sleep(1)
