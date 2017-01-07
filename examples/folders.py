from nessus.api.models import Folder
from nessus.client import NessusClient
from nessus.exceptions import NessusApiException


def example(test_name):

    # Generate unique names.
    scan_name = test_name(u'my test scan')
    folder_name = test_name(u'my test folder', length=5)

    '''
    Instantiate an instance of the NessusClient.
    '''
    client = NessusClient()

    '''
    Create a folder.
    '''
    folder = client.folder_helper.create(
        name=folder_name
    )
    assert folder.name() == folder_name

    '''
    Create a scan for testing.
    '''
    scan = client.scan_helper.create(
        name=scan_name,
        text_targets='tenable.com',
        template='discovery'
    )

    '''
    Move scan to the newly created folder (method A).
    '''
    assert scan.folder().id != folder.id
    scan.move_to(folder)
    assert scan.folder().id == folder.id

    '''
    Move scan to trash (method A).
    '''
    scan.trash()
    assert scan.folder().id != folder.id

    '''
    Move scan to the newly created folder (method B).
    '''
    folder.add(scan)
    assert scan.folder().id == folder.id

    '''
    Move scan to trash (method B).
    '''
    trash_folder = client.folder_helper.trash_folder()
    trash_folder.add(scan)
    assert scan.folder().id == trash_folder.id

    '''
    Move scan to the main folder "My Scans".
    '''
    main_folder = client.folder_helper.main_folder()
    main_folder.add(scan)
    assert scan.folder().type() == Folder.TYPE_MAIN

    '''
    Stop all scans in folder.
    '''
    folder.add(scan)
    scan.launch()
    assert not scan.stopped()
    folder.stop_scans()
    assert scan.stopped()

    '''
    Delete folder and scan.
    '''
    folder.delete()
    scan.delete()
    assert client.folder_helper.id(folder.id) is None
    try:
        scan.details()
        assert False
    except NessusApiException:
        pass
