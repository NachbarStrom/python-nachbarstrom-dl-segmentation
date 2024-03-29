import os
import pathlib
from google.cloud import storage

from .file_updater import FileUpdater, UpdatePromise


class GoogleStorageFileUpdater(FileUpdater):

    BUCKET_NAME = "tms-solai-1521560021665.appspot.com"
    DESTINATION_FOLDER = "model"

    def __init__(self, storage_client=None):
        if storage_client is None:
            json_credentials_path = \
                os.path.join("cred", "google_service_account.json")
            storage_client = storage.Client.from_service_account_json(
                json_credentials_path)
        self._bucket = storage_client.get_bucket(self.BUCKET_NAME)
        self._local_file_path = None

    def update_file(self, file_name: str) -> UpdatePromise:
        self._update_local_file_path(file_name=file_name)
        self._check_destination_folder_exists()
        if not os.path.exists(self._local_file_path):
            self._download_file(file_name)
        return UpdatePromise()

    def _check_destination_folder_exists(self):
        pathlib.Path(self.DESTINATION_FOLDER).mkdir(parents=True, exist_ok=True)

    def _download_file(self, file_name):
        blob = self._bucket.get_blob(file_name)
        blob.download_to_filename(self._local_file_path)
        print("File '%s' downloaded from google storage." % file_name)

    def _update_local_file_path(self, file_name: str):
        self._local_file_path = os.path.join(self.DESTINATION_FOLDER,
                                             file_name)


if __name__ == '__main__':
    mock_models = [
        "delme1.txt",
        "delme2.txt",
        "delme3.txt"
    ]
    for model in mock_models:
        GoogleStorageFileUpdater().update_file(model)
