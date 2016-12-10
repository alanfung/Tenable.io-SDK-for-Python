import pytest
from time import sleep

from nessus.exceptions import NessusException
from nessus.resources.models import Scan, ScanList, ScanSettings
from nessus.resources.scans import ScanCreateRequest

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
            self._wait_scan_status(client, scan_id, [Scan.STATUS_CANCELED, Scan.STATUS_COMPLETED, Scan.STATUS_EMPTY])
            client.scans.delete(scan_id)

    def test_list_return_correct_type(self, client):
        scan = client.scans.list()
        assert isinstance(scan, ScanList), u'The `list` method returns type.'

    def test_create_launch_pause_resume_stop_delete(self, client, scan_id):
        scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_CANCELED, Scan.STATUS_COMPLETED, Scan.STATUS_EMPTY], \
            u'Scan is in idling state.'

        client.scans.launch(scan_id)

        scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_PENDING, Scan.STATUS_RUNNING], u'Scan is in launched state.'

        scan_details = self._wait_scan_status(client, scan_id, [Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])
        assert scan_details.info.status == Scan.STATUS_RUNNING, u'Scan should be running to test pause.'

        client.scans.pause(scan_id)
        scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_PAUSED, Scan.STATUS_PAUSING], u'Scan is pausing.'

        scan_details = self._wait_scan_status(client, scan_id, [Scan.STATUS_PAUSED])
        assert scan_details.info.status == Scan.STATUS_PAUSED, u'Scan is paused.'

        client.scans.resume(scan_id)
        scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_RESUMING, Scan.STATUS_RUNNING], u'Scan is resuming.'

        scan_details = self._wait_scan_status(client, scan_id, [Scan.STATUS_COMPLETED, Scan.STATUS_RUNNING])
        assert scan_details.info.status == Scan.STATUS_RUNNING, u'Scan is running.'

        client.scans.stop(scan_id)
        scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in [Scan.STATUS_CANCELED, Scan.STATUS_STOPPING], u'Scan is resuming.'

        scan_details = self._wait_scan_status(client, scan_id, [Scan.STATUS_CANCELED])
        assert scan_details.info.status == Scan.STATUS_CANCELED, u'Scan is canceled.'

    @staticmethod
    def _wait_scan_status(client, scan_id, statuses):
        scan_details = client.scans.details(scan_id)
        max_check = 20
        while scan_details.info.status not in statuses and max_check > 0:
            sleep(2 + max_check)
            max_check -= 1
            scan_details = client.scans.details(scan_id)
        assert scan_details.info.status in statuses, u'Timeout waiting for scan status'
        return scan_details
