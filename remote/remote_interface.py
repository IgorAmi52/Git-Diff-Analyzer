from abc import abstractmethod


class RemoteInterface:
    @abstractmethod
    def __check_connection(self):
        pass

    @abstractmethod
    def get_latest_commit(self, branch):
        pass

    @abstractmethod
    def get_changed_files(self, base_commit_hash, commit_hash):
        pass
