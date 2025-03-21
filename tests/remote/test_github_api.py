# tests/services/test_github_api.py
import pytest
from unittest.mock import patch, Mock
from remote.github_api import GithubAPI


# Test for successful connection to GitHub API
@patch('requests.get')
def test_check_connection_success(mock_get):
    """Test successful connection to GitHub repository."""
    # Mock the response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Create the GithubAPI object
    # Should not raise ValueError
    github_api = GithubAPI("owner", "repo", "access_token")


# Test for failed connection to GitHub API
@patch('requests.get')
def test_check_connection_failure(mock_get):
    """Test failed connection to GitHub repository."""
    # Mock the response object
    mock_response = Mock()
    mock_response.status_code = 404  # Not Found
    mock_get.return_value = mock_response

    # Create the GithubAPI object, Check if the connection raises an exception
    with pytest.raises(ValueError):
        GithubAPI("owner", "repo", "access_token")


# Test for successfully fetching commits after a commit hash
@patch('requests.get')
def test_get_after_commits_success(mock_get):
    """Test fetching commits after a given commit hash."""
    # Mock the response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"sha": "commit1", "commit": {"message": "First commit"}},
        {"sha": "commit2", "commit": {"message": "Second commit"}}
    ]
    mock_get.return_value = mock_response

    # Create the GithubAPI object
    github_api = GithubAPI("owner", "repo", "access_token")

    # Fetch commits after a given commit hash
    commits = github_api.get_after_commits("main", "merge_base_commit_hash")

    # Check the response
    assert len(commits) == 2
    assert commits[0]['sha'] == "commit1"
    assert commits[1]['commit']['message'] == "Second commit"


# Test for failed commit fetch
@patch('requests.get')
def test_get_after_commits_failure(mock_get):
    """Test failed commit fetch when GitHub API returns an error."""
    # Mock the response objects
    mock_get.side_effect = [Mock(status_code=200), Mock(status_code=400)]

    # Create the GithubAPI object
    github_api = GithubAPI("owner", "repo", "access_token")

    # Fetch commits after a given commit hash, should return None on failure
    commits = github_api.get_after_commits("main", "merge_base_commit_hash")

    # Check the result (should be None)
    assert commits is None
