import pytest
from unittest.mock import patch, Mock
from remote.github_api import GithubAPI


@pytest.fixture
@patch('remote.github_api.GithubAPI._make_request')
def github_api(mock_make_request):
    """Fixture for GithubAPI that mocks the connection call."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_make_request.return_value = mock_response
    return GithubAPI("owner", "repo", "access_token")


def test_check_connection_success(github_api):
    """Test successful connection to GitHub repository."""
    assert github_api is not None


@patch('remote.github_api.GithubAPI._make_request')
def test_check_connection_failure(mock_make_request):
    """Test failed connection to GitHub repository."""
    mock_make_request.side_effect = ValueError("Failed to connect to GitHub")
    with pytest.raises(ValueError):
        GithubAPI("owner", "repo", "access_token")


@patch("remote.github_api.GithubAPI._make_request")
def test_get_latest_commit_success(mock_make_request, github_api):
    """Test fetching the latest commit on a given branch."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"commit": {"sha": "commit1"}}
    mock_make_request.return_value = mock_response

    commit = github_api.get_latest_commit("main")

    assert commit == "commit1"


@patch("remote.github_api.GithubAPI._make_request")
def test_get_latest_commit_failure(mock_make_request, github_api):
    """Test failed commit fetch when GitHub API returns an error."""
    mock_make_request.side_effect = ValueError(
        "Failed to fetch the latest commit from GitHub.")
    with pytest.raises(ValueError, match="Failed to fetch the latest commit from GitHub."):
        github_api.get_latest_commit("main", )


@patch("remote.github_api.GithubAPI._make_request")
def test_get_changed_files_success(mock_make_request, github_api):
    """Test fetching changed files between two commits."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "files": [
            {"filename": "file1.py"},
            {"filename": "file2.py"}
        ]
    }
    mock_make_request.return_value = mock_response

    changed_files = github_api.get_changed_files(
        "base_commit_hash", "commit_hash")

    assert len(changed_files) == 2
    assert "file1.py" in changed_files
    assert "file2.py" in changed_files


@patch("remote.github_api.GithubAPI._make_request")
def test_get_changed_files_failure(mock_make_request, github_api):
    """Test failed fetch of changed files when GitHub API returns an error."""
    mock_make_request.side_effect = ValueError(
        "Failed to fetch changed files: 404 - Not Found")
    with pytest.raises(ValueError):
        github_api.get_changed_files("base_commit_hash", "commit_hash")


@patch("remote.github_api.GithubAPI._make_request")
def test_get_file_content_success(mock_make_request, github_api):
    """Test fetching file content from a commit."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"content": "file content"}
    mock_make_request.return_value = mock_response

    content = github_api.get_file_content("commit_sha", "file_path")
    assert content == "file content"


@patch("remote.github_api.GithubAPI._make_request")
def test_get_file_content_failure(mock_make_request, github_api):
    """Test failed fetch of file content when GitHub API returns an error."""
    mock_make_request.side_effect = ValueError(
        "Failed to fetch file content: 404 - Not Found")
    with pytest.raises(FileNotFoundError):
        github_api.get_file_content("commit_sha", "file_path")


@patch("remote.github_api.GithubAPI.get_file_content")
def test_is_diff_different(mock_get_file_content, github_api):
    """Test successful diff check between two files."""
    mock_get_file_content.side_effect = ["file1 content", "file2 content"]
    is_diff = github_api.is_diff("commit1", "file1", "commit2", "file2")
    assert is_diff is True


@patch("remote.github_api.GithubAPI.get_file_content")
def test_is_diff_same(mock_get_file_content, github_api):
    """Test failed diff check when file content fetch fails."""
    mock_get_file_content.side_effect = [
        ValueError("File not found"), "file2 content"]
    result = github_api.is_diff("commit1", "file1", "commit2", "file2")
    assert result is False
