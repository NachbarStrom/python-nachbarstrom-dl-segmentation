import threading

from .file_updater import FileUpdater, UpdatePromise


class AsyncUpdatePromise(UpdatePromise, threading.Thread):
    """A thread that runs the file update in the background"""

    def __init__(self, file_updater: FileUpdater, file_name: str) -> None:
        super().__init__()
        self._file_name = file_name
        self._file_updater = file_updater

    def run(self):
        self._file_updater.update_file(self._file_name)

    def wait_until_update_complete(self) -> None:
        self.join()


class AsyncFileUpdater(FileUpdater):
    """
    A file updater whose update method runs asynchronous in the
    background. It takes any other FileUpdater implementation in the
    constructor and delegates to it the file update.
    """

    def __init__(self, file_updater_delegate: FileUpdater) -> None:
        assert file_updater_delegate is not None
        self._file_updater_delegate = file_updater_delegate

    def update_file(self, file_name: str) -> UpdatePromise:
        promise = AsyncUpdatePromise(self._file_updater_delegate, file_name)
        promise.start()
        return promise
