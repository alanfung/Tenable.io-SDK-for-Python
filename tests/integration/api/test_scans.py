import pytest
from time import sleep

from nessus.exceptions import NessusException
from nessus.api.models import Scan, ScanList, ScanSettings
from nessus.api.scans import ScansApi, ScanCreateRequest, ScanExportRequest

from tests.base import BaseTest
from tests.config import NessusTestConfig


class TestScansResource(BaseTest):

    @pytest.fixture(scope='class')
    def template(self, client):
        """
        Get scan template for testing.
        """
        template_list = client.editor.list('scan')
        assert len(template_list.templates) > 0, u'At least one scan template.'

        test_templates = [t for t in template_list.templates if t.name == NessusTestConfig.get('scan_template_name')]
        assert len(test_templates) > 0

        yield test_templates[0]

    @pytest.fixture(scope='class')
    def scan_id(self, app, client, template):
        """
        Create a scan for testing.
        """
        scan_id = client.scans.create(
            ScanCreateRequest(
                template.uuid,
                ScanSettings(
                    app.session_name('test_scans'),
                    NessusTestConfig.get('scan_text_targets'),
                )
            )
        )
        yield scan_id

        try:
            client.scans.delete(scan_id)
        except NessusException:
            # This happens when the scan is not idling.
            client.scans.stop(scan_id)
            self.wait_until(lambda: client.scans.details(scan_id),
                            lambda details: details.info.status in
                                            [Scan.STATUS_CANCELED, Scan.STATUS_COMPLETED, Scan.STATUS_EMPTY])
            client.scans.delete(scan_id)

    def test_list_return_correct_type(self, client):
        scan = client.scans.list()
        assert isinstance(scan, ScanList), u'The `list` method returns type.'

    def test_create_launch_pause_resume_stop_delete(self, client, scan_id):
        scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_CANCELED, Scan.STATUS_COMPLETED, Scan.STATUS_EMPTY], \
            u'Scan is in idling state.'

        # Launch the scan.
        client.scans.launch(scan_id)
        scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_PENDING, Scan.STATUS_RUNNING], u'Scan is in launched state.'

        scan_details = self.wait_until(lambda: client.scans.details(scan_id),
                                       lambda details: details.info.status in [
                                           Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])
        assert scan_details.info.status == Scan.STATUS_RUNNING, u'Scan should be running to test pause.'

        # Pause the running scan.
        client.scans.pause(scan_id)
        scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_PAUSED, Scan.STATUS_PAUSING], u'Scan is pausing.'
        scan_details = self.wait_until(lambda: client.scans.details(scan_id),
                                       lambda details: details.info.status in [Scan.STATUS_PAUSED])
        assert scan_details.info.status == Scan.STATUS_PAUSED, u'Scan is paused.'

        # Resume the paused scan.
        client.scans.resume(scan_id)
        scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_RESUMING, Scan.STATUS_RUNNING], u'Scan is resuming.'

        scan_details = self.wait_until(lambda: client.scans.details(scan_id),
                                       lambda details: details.info.status in [
                                           Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])
        assert scan_details.info.status == Scan.STATUS_RUNNING, u'Scan is running.'

        # Stop the running scan.
        client.scans.stop(scan_id)
        scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_CANCELED, Scan.STATUS_STOPPING], u'Scan is resuming.'

        scan_details = self.wait_until(lambda: client.scans.details(scan_id),
                                       lambda details: details.info.status in [Scan.STATUS_CANCELED])
        assert scan_details.info.status == Scan.STATUS_CANCELED, u'Scan is canceled.'

    def test_export(self, client, scan_id):

        # Cannot export on a test that has never been launched, therefore launch the scan first.
        client.scans.launch(scan_id)
        self.wait_until(lambda: client.scans.details(scan_id),
                        lambda details: details.info.status in [Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])

        # Stop the running scan.
        client.scans.stop(scan_id)
        self.wait_until(lambda: client.scans.details(scan_id),
                        lambda details: details.info.status in [Scan.STATUS_CANCELED])

        file_id = client.scans.export_request(
            scan_id,
            ScanExportRequest(
                format=ScanExportRequest.FORMAT_PDF
            )
        )
        assert file_id, u'The `export_request` method returns a valid file ID.'

        export_status = self.wait_until(lambda: client.scans.export_status(scan_id, file_id),
                                        lambda status: status == ScansApi.STATUS_EXPORT_READY)
        assert export_status == ScansApi.STATUS_EXPORT_READY, u'Scan export is ready.'

        iter_content = client.scans.export_download(scan_id, file_id, False, None)
        assert len(list(iter_content)), u'The `export_download` method return non-empty iterable content.'
