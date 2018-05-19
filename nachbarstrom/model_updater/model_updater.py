class UpdatePromise:
    """A promise about whether the update is completed"""

    def wait_until_update_complete(self) -> None:
        """Makes the system wait until the update is complete."""
        raise NotImplementedError


class ModelUpdater:
    def update_model(self, model_name: str) -> UpdatePromise:
        """
        Updates the input model to its latest version.
        :param model_name: Name of the model.
        :return: A promise that describes the current state of the
        model update.
        """
        raise NotImplementedError
