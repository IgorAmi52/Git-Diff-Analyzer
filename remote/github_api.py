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
            raise ValueError(f"Failed to connect to the GitHub repository. Status code: {response.status_code}")

    def get_after_commits(self, branch, commit_hash):
        """Fetch all commits after the given commit hash."""
        url = f"{self.base_url}/commits"
        headers = {"Authorization": f"token {self.access_token}"}
        params = {"sha": branch, "since": commit_hash}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            commits = response.json()
            return commits
        else:
            print(f"Error fetching commits from GitHub API: {response.status_code}")
            return None
