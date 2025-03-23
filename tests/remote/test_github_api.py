import pytest
from unittest.mock import patch, Mock
from remote.github_api import GithubAPI


# Fixture to create a GithubAPI instance with a mocked connection
@pytest.fixture
@patch('requests.get')
def github_api(mock_get):
    """Fixture for GithubAPI that mocks the connection call."""
    # Mock the response object for connection during initialization
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Return the mocked GithubAPI instance
    return GithubAPI("owner", "repo", "access_token")


# Test for successful connection to GitHub API
@patch('requests.get')
def test_check_connection_success(github_api):
    """Test successful connection to GitHub repository."""
    # The connection should succeed due to our mock in the fixture
    assert github_api is not None


# Test for failed connection to GitHub API
@patch('requests.get')
def test_check_connection_failure(mock_get):
    """Test failed connection to GitHub repository."""
    # Mock the response object to simulate a 404 error
    mock_response = Mock()
    mock_response.status_code = 404  # Not Found
    mock_get.return_value = mock_response

    # Check if the connection raises an exception
    with pytest.raises(ValueError):
        GithubAPI("owner", "repo", "access_token")


# Test for successfully fetching commit
@patch('requests.get')
def test_get_latest_commit_success(mock_get, github_api):
    """Test fetching the latest commit on a given branch."""
    # Mock the response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"commit": {"sha": "commit1"}}
    mock_get.return_value = mock_response

    # Fetch commits after a given commit hash
    commit = github_api.get_latest_commit("main")

    # Check the response
    assert commit == "commit1"


# Test for failed commit fetch
@patch('requests.get')
def test_get_latest_commit_failure(mock_get, github_api):
    """Test failed commit fetch when GitHub API returns an error."""
    # Mock the response objects
    mock_get.return_value = Mock(status_code=404)
    with pytest.raises(ValueError, match="Failed to fetch the latest commit from GitHub."):
        github_api.get_latest_commit("main", )


# Test for successfully fetching changed files between two commits
@patch('requests.get')
def test_get_changed_files_success(mock_get, github_api):
    """Test fetching changed files between two commits."""
    # Mock the response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "files": [
            {"filename": "file1.py"},
            {"filename": "file2.py"}
        ]
    }
    mock_get.return_value = mock_response

    # Fetch changed files
    changed_files = github_api.get_changed_files(
        "base_commit_hash", "commit_hash")

    # Check the response
    assert len(changed_files) == 2
    assert "file1.py" in changed_files
    assert "file2.py" in changed_files


# Test for failed fetch of changed files
@patch('requests.get')
def test_get_changed_files_failure(mock_get, github_api):
    """Test failed fetch of changed files when GitHub API returns an error."""
    # Mock the response object
    mock_response = Mock()
    mock_response.status_code = 404  # Not Found
    mock_response.text = "Not Found"
    mock_get.return_value = mock_response

    # Attempt to fetch changed files, should raise ValueError
    with pytest.raises(ValueError, match="Failed to fetch changed files: 404 - Not Found"):
        github_api.get_changed_files("base_commit_hash", "commit_hash")
