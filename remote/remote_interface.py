from abc import abstractmethod


class RemoteInterface:
    @abstractmethod
    def __check_connection(self):
        pass

    @abstractmethod
    def get_after_commits(commit_hash):
        pass
