import os
import pytest
from time import time

from nessus.helpers.scan import ScanRef

from tests.base import BaseTest
from tests.config import NessusTestConfig


class TestScanHelper(BaseTest):

    @pytest.fixture(scope='class')
    def scan(self, app, client):
        """
        Create a scan for testing.
        """
        scan = client.scan_helper.create(
            app.session_name('test_scan'),
            NessusTestConfig.get('scan_text_targets'),
            NessusTestConfig.get('scan_template_name'))
        yield scan
        scan.delete()

    def test_details(self, scan):
        scan_detail = scan.details()
        assert scan_detail.info.object_id == scan.id, u'ScanRef `id` should match ID in ScanDetail.'

    def test_launch_stop_download(self, app, scan):
        download_path = app.session_file_output('test_scan_launch_download')

        assert not os.path.isfile(download_path), u'Scan report does not yet exist.'
        scan.launch().stop().download(download_path)

        assert os.path.isfile(download_path), u'Scan report is downloaded.'
        os.remove(download_path)
        assert not os.path.isfile(download_path), u'Scan report is deleted.'

    def test_cancel_after(self, scan):
        cancel_after_seconds = 10

        start_time = time()
        scan.launch().wait_or_cancel_after(cancel_after_seconds)
        stop_time = time()

        assert stop_time - start_time >= cancel_after_seconds, \
            u'Scan is ran for at least %s seconds.' % cancel_after_seconds
        assert scan.status() in ScanRef.STATUSES_STOPPED, u'Scan is stopped.'
