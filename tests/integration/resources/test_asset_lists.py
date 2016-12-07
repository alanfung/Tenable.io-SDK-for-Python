import pytest

from nessus.client import NessusClient
from nessus.resources.asset_lists import AssetListCreateRequest
from nessus.resources.models import AssetList, AssetListList


class TestAssetLists(object):

    @pytest.fixture(scope='class')
    def asset_list(self, app):
        asset_list = NessusClient().asset_lists.create(AssetListCreateRequest(
            name=app.session_name('test_asset_lists'),
            members='tenable.com',
            type='system',
        ))
        yield asset_list
        assert NessusClient().asset_lists.delete(asset_list.id), u'Asset list is deleted.'

    def test_list_return_correct_type(self):
        asset_list_list = NessusClient().asset_lists.list()
        assert isinstance(asset_list_list, AssetListList), u'The `list` method return type.'

    def test_create_delete(self, app):
        asset_list = NessusClient().asset_lists.create(AssetListCreateRequest(
            name=app.session_name('test_create_delete'),
            members='tenable.com',
            type='system',
        ))
        assert isinstance(asset_list, AssetList), u'The `create` method return type.'
        assert hasattr(asset_list, 'id'), u'Asset list has ID.'
        assert NessusClient().asset_lists.delete(asset_list.id), u'Asset list is deleted.'

    def test_get(self, asset_list):
        got_asset_list = NessusClient().asset_lists.details(asset_list.id)
        assert got_asset_list.id == asset_list.id, u'The `details` method returns asset list with matching IDs.'

    def test_list(self, asset_list):
        asset_list_list = NessusClient().asset_lists.list()
        for l in asset_list_list.asset_lists:
            assert isinstance(l, AssetList), u'Asset list list\'s element type.'
        assert len([l for l in asset_list_list.asset_lists if l.id == asset_list.id]) == 1, \
            u'Asset list list contains created access list.'
