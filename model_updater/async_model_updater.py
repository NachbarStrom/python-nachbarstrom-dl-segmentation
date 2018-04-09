import threading

from model_updater import ModelUpdater, UpdatePromise


class AsyncUpdatePromise(UpdatePromise, threading.Thread):
    """A thread that runs the model update in the background"""

    def __init__(self, model_updater: ModelUpdater, model_name: str):
        super().__init__()
        self._model_name = model_name
        self._model_updater = model_updater

    def run(self):
        self._model_updater.update_model(self._model_name)

    def wait_until_update_complete(self) -> None:
        self.join()


class AsyncModelUpdater(ModelUpdater):
    """
    A model updater whose update method runs asynchronous in the
    background. It takes any other model updater implementation in the
    constructor and delegates to it the model updating.
    """

    def __init__(self, model_updater_delegate: ModelUpdater):
        assert model_updater_delegate is not None
        self._model_updater_delegate = model_updater_delegate

    def update_model(self, model_name: str) -> UpdatePromise:
        promise = AsyncUpdatePromise(self._model_updater_delegate, model_name)
        promise.start()
        return promise
