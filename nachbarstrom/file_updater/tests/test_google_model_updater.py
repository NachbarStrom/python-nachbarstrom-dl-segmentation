from unittest.mock import MagicMock

from .. import GoogleStorageFileUpdater


def test_construction():
    storage_client = MagicMock()
    file_name = "mock"
    GoogleStorageFileUpdater(storage_client).update_file(file_name)
