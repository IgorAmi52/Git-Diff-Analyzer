import pytest
from unittest.mock import patch, Mock
from git_utils.git_commands import *


# Test successful merge base retrieval
@patch('subprocess.run')
def test_get_merge_base_success(mock_run):
    mock_run.return_value = Mock(returncode=0,
                                 stdout='abc123',
                                 stderr='')

    branch_a = 'branchA'
    branch_b = 'branchB'
    repo_loc = '/path/to/repo'
    result = get_merge_base(branch_a, branch_b, repo_loc)

    # Assert that the result matches the mocked merge base hash
    assert result == 'abc123'
    mock_run.assert_called_once_with(['git',
                                      'merge-base',
                                      branch_a,
                                      branch_b],
                                     cwd=repo_loc,
                                     capture_output=True,
                                     text=True)


# Test failure when merge base cannot be retrieved
@patch('subprocess.run')
def test_get_merge_base_failure(mock_run):
    mock_run.return_value = Mock(
        returncode=1, stdout='', stderr='Error message')

    with pytest.raises(ValueError,
                       match='Error in getting merge base: Error message'):
        get_merge_base('branchA', 'branchB', '/path/to/repo')

    # Assert that subprocess.run was called with the correct parameters
    mock_run.assert_called_once_with(['git',
                                      'merge-base',
                                      'branchA',
                                      'branchB'],
                                     cwd='/path/to/repo',
                                     capture_output=True,
                                     text=True)


@patch('subprocess.run')
def test_get_local_last_commit_success(mock_run):
    """Test successful retrieval of the last commit hash."""
    # Mock the subprocess result
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "abc123\n"
    mock_run.return_value = mock_result

    # Call the function
    commit_hash = get_local_last_commit("main", "/path/to/repo")

    # Check the result
    assert commit_hash == "abc123"


# Test for failure in retrieving the last commit hash
@patch('subprocess.run')
def test_get_local_last_commit_failure(mock_run):
    """Test failure in retrieving the last commit hash."""
    # Mock the subprocess result
    mock_result = Mock()
    mock_result.returncode = 1
    mock_result.stderr = "fatal: ambiguous argument 'refs/heads/main': unknown revision"
    mock_run.return_value = mock_result

    # Call the function and expect a ValueError
    with pytest.raises(ValueError, match="Error retrieving last commit: fatal: ambiguous argument 'refs/heads/main': unknown revision"):
        get_local_last_commit("main", "/path/to/repo")


# Test for successfully retrieving changed files between two commits
@patch('subprocess.run')
def test_get_changed_files_success(mock_run):
    """Test successful retrieval of changed files."""
    # Mock the subprocess result
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "file1.py\nfile2.py\n"
    mock_run.return_value = mock_result

    # Call the function
    changed_files = get_changed_files("/path/to/repo", "abc123", "def456")

    # Check the result
    assert changed_files == ["file1.py", "file2.py"]


# Test for failure in retrieving changed files
@patch('subprocess.run')
def test_get_changed_files_failure(mock_run):
    """Test failure in retrieving changed files."""
    # Mock the subprocess result
    mock_result = Mock()
    mock_result.returncode = 1
    mock_result.stderr = "fatal: bad revision 'abc123..def456'"
    mock_run.return_value = mock_result

    # Call the function and expect a ValueError
    with pytest.raises(ValueError, match="Error retrieving changed files: fatal: bad revision 'abc123..def456'"):
        get_changed_files("/path/to/repo", "abc123", "def456")
