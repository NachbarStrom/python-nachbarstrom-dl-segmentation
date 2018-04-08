from unittest.mock import MagicMock

from model_updater import GoogleStorageModelUpdater


def test_construction():
    storage_client = MagicMock()
    model_name = "mock"
    GoogleStorageModelUpdater(storage_client).update_model(model_name)
