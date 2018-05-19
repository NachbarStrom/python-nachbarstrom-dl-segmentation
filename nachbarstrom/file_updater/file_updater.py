class UpdatePromise:
    """A promise about whether the update is completed"""

    def wait_until_update_complete(self) -> None:
        """Makes the system wait until the update is complete."""
        pass


class FileUpdater:
    def update_file(self, file_name: str) -> UpdatePromise:
        """
        Updates the input file to its latest version.
        :param file_name: The file to update.
        :return: A promise that describes the current state of the
        update.
        """
        raise NotImplementedError
