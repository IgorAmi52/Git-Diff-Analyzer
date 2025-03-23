import requests

from remote.remote_interface import RemoteInterface


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

    def __check_connection(self):
        """Check if the provided GitHub
        credentials and repository are valid."""
        url = f"{self.base_url}"
        headers = {"Authorization": f"token {self.access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Successfully connected to GitHub repository.")
        else:
            raise ValueError(
                f"Failed to connect to the GitHub repository. Status code: {response.status_code}")

    def get_latest_commit(self, branch):
        """Fetch the latest commit on the given branch."""
        url = f"{self.base_url}/branches/{branch}"
        headers = {"Authorization": f"token {self.access_token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['commit']['sha']
        else:
            raise ValueError("Failed to fetch the latest commit from GitHub.")

    def get_changed_files(self, base_commit_hash, commit_hash):
        """Get a list of changed files between two commits on GitHub."""
        url = f"{self.base_url}/compare/{base_commit_hash}...{commit_hash}"
        headers = {"Authorization": f"token {self.access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise ValueError(
                f"Failed to fetch changed files: {response.status_code} - {response.text}")

        changed_files = response.json().get("files", [])
        return [file["filename"] for file in changed_files]
