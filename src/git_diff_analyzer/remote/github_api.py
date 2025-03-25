import logging
import requests

from git_diff_analyzer.remote.remote_interface import RemoteInterface

logger = logging.getLogger(__name__)


class GithubAPI(RemoteInterface):
    def __init__(self, owner, repo, access_token):
        """
        Initialize the GitHubAPI object with the
        repository owner, name, and personal access token.
        """
        self.owner = owner
        self.repo = repo
        self.access_token = access_token
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.__check_connection()

    def _make_request(self, method, endpoint, params=None):
        """Helper function to make API requests and handle errors."""
        url = self.base_url if not endpoint else f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"token {self.access_token}"}
        if params is None:
            response = requests.request(method, url, headers=headers)
        else:
            response = requests.request(
                method, url, headers=headers, params=params)

        if response.status_code == 200:
            return response

        error_msg = response.json().get("message", "Unknown error")
        raise ValueError(f"GitHub API request failed: {error_msg}")

    def __check_connection(self):
        """Check if the connection to GitHub is successful."""
        try:
            self._make_request("GET", "").json()
        except ValueError:
            logger.error(
                "Failed to connect to the GitHub repository", exc_info=True)
            raise

    def get_latest_commit(self, branch):
        try:
            response = self._make_request("GET", f"branches/{branch}")
            return response.json()['commit']['sha']
        except ValueError:
            raise ValueError("Failed to fetch the latest commit from GitHub.")

    def get_changed_files(self, base_commit_hash, commit_hash):
        try:
            response = self._make_request(
                "GET", f"compare/{base_commit_hash}...{commit_hash}")
            changed_files = response.json().get("files", [])
            return [file["filename"] for file in changed_files]
        except ValueError as e:
            logger.error("Failed to fetch changed files: %s", e)
            raise ValueError(
                "Failed to fetch changed files.")

    def get_file_content(self, commit_sha, file_path):
        try:
            params = {"ref": commit_sha}
            response = self._make_request(
                "GET", f"contents/{file_path}", params)
            return response.json().get("content")
        except ValueError:
            # Handle case when the file does not exist in this commit
            raise FileNotFoundError(
                f"File '{file_path}' not found in commit {commit_sha}.")

    def is_diff(self, commit_a, file_a, commit_b, file_b):
        try:
            content_a = self.get_file_content(commit_a, file_a)
            content_b = self.get_file_content(commit_b, file_b)
            return content_a != content_b
        except ValueError as e:
            logger.error("Error in checking diff remote: %s", e)
            return False
