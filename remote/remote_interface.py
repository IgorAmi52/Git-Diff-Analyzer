from abc import abstractmethod


class RemoteInterface:
    @abstractmethod
    def __check_connection(self):
        # Check if the provided credentials and repository are valid
        pass

    @abstractmethod
    def get_latest_commit(self, branch):
        # Fetch the latest commit on the given branch
        pass

    @abstractmethod
    def get_changed_files(self, base_commit_hash, commit_hash):
        # Get a list of changed files between two commits
        pass

    @abstractmethod
    def is_diff(self, commit_a, file_ca, commit_b, file_cb):
        # Check if the file content in two commits is the same. Returns false if identical
        pass
