import os

from datetime import datetime
from time import time

from nessus.api.models import Scan
from nessus.exceptions import NessusApiException
from nessus.client import NessusClient


def example(test_name, test_file):

    # Generate unique name and file.
    scan_name = test_name(u'my test scan')
    test_file_output = test_file(u'my_test_report.pdf')

    '''
    Instantiate an instance of the NessusClient.
    '''
    client = NessusClient()

    '''
    Create a scan.
    '''
    scan = client.scan_helper.create(
        name=scan_name,
        text_targets='tenable.com',
        template='discovery'
    )
    assert scan.name() == scan_name

    '''
    Retrieve a scan by ID.
    '''
    scan_b = client.scan_helper.id(scan.id)
    assert scan_b is not scan
    assert scan_b.name() == scan_name

    '''
    Select scans by name.
    '''
    scans = client.scan_helper.scans(name=scan_name)
    assert scans[0].name() == scan_name

    '''
    Select scans by name with regular expression.
    '''
    scans = client.scan_helper.scans(name_regex=r'.*test scan.*')
    assert len(scans) > 0

    '''
    Launch a scan, then download when scan is completed.
    Note: The `download` method blocks until the scan is completed and the report is downloaded.
    '''
    scan.launch().download(test_file_output)
    assert os.path.isfile(test_file_output)
    os.remove(test_file_output)

    '''
    Launch a scan, pause it, resume it, then stop it.
    '''
    scan.launch().pause()
    assert scan.status() == Scan.STATUS_PAUSED
    scan.resume().stop()
    assert scan.status() == Scan.STATUS_CANCELED

    '''
    Stop a running scan if it does not complete within a specific duration.
    '''
    start = time()
    scan.launch().wait_or_cancel_after(10)
    assert time() - start >= 10

    '''
    Retrieve the history of a scan since a specific date or all.
    Note: The `since` argument is optional, all the history if omitted.
    '''
    histories = scan.histories(since=datetime(2016, 12, 1))
    assert len(histories) > 0

    '''
    Download the report for a specific scan in history.
    '''
    scan.download(test_file_output, history_id=histories[0].history_id)
    assert os.path.isfile(test_file_output)
    os.remove(test_file_output)

    '''
    Create a new scan by copying a scan.
    '''
    scan_copy = scan.copy()
    assert scan_copy.id != scan.id
    assert scan_copy.status() == Scan.STATUS_EMPTY

    '''
    Delete scans.
    '''
    scan.delete()
    scan_copy.delete()
    try:
        scan.details()
        assert False
    except NessusApiException:
        pass
    try:
        scan_copy.details()
        assert False
    except NessusApiException:
        pass
