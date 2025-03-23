import pytest
from unittest.mock import patch, Mock
from git_utils.git_commands import *


@patch('subprocess.run')
def test_run_git_command_success(mock_run):
    """Test successful execution of a git command."""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "output\n"
    mock_run.return_value = mock_result

    output = run_git_command(["git", "status"], "/path/to/repo")
    assert output == "output"


@patch('subprocess.run')
def test_run_git_command_failure(mock_run):
    """Test failure in executing a git command."""
    mock_result = Mock()
    mock_result.returncode = 1
    mock_result.stderr = "fatal: not a git repository"
    mock_run.return_value = mock_result

    with pytest.raises(ValueError, match="Git command failed: fatal: not a git repository"):
        run_git_command(["git", "status"], "/path/to/repo")


@patch('git_utils.git_commands.run_git_command')
def test_get_merge_base_success(mock_run_git_command):
    """Test successful retrieval of the merge base."""
    mock_run_git_command.return_value = "abc123"
    branch_a = 'branchA'
    branch_b = 'branchB'
    repo_loc = '/path/to/repo'
    result = get_merge_base(branch_a, branch_b, repo_loc)
    assert result == 'abc123'


@patch('git_utils.git_commands.run_git_command')
def test_get_merge_base_failure(mock_run_git_command):
    """Test failure in retrieving the merge base."""
    mock_run_git_command.side_effect = ValueError("Error message")

    with pytest.raises(ValueError):
        get_merge_base('branchA', 'branchB', '/path/to/repo')


@patch('git_utils.git_commands.run_git_command')
def test_get_local_last_commit_success(mock_run_git_command):
    """Test successful retrieval of the last commit hash."""
    mock_run_git_command.return_value = "abc123"
    commit_hash = get_local_last_commit("main", "/path/to/repo")
    assert commit_hash == "abc123"


@patch('git_utils.git_commands.run_git_command')
def test_get_local_last_commit_failure(mock_run_git_command):
    """Test failure in retrieving the last commit hash."""
    mock_run_git_command.side_effect = ValueError("Error message")
    with pytest.raises(ValueError):
        get_local_last_commit("main", "/path/to/repo")


@patch('git_utils.git_commands.run_git_command')
def test_get_changed_files_success(mock_run_git_command):
    """Test successful retrieval of changed files."""
    mock_run_git_command.return_value = "file1.py\nfile2.py"
    changed_files = get_changed_files("/path/to/repo", "abc123", "def456")
    assert changed_files == ["file1.py", "file2.py"]


@patch('git_utils.git_commands.run_git_command')
def test_get_changed_files_failure(mock_run_git_command):
    """Test failure in retrieving changed files."""
    mock_run_git_command.side_effect = ValueError("Error message")

    with pytest.raises(ValueError):
        get_changed_files("/path/to/repo", "abc123", "def456")


@patch('git_utils.git_commands.run_git_command')
def test_get_file_exists_success(mock_run_git_command):
    """Test successful file existence check."""
    mock_run_git_command.return_value = "100644 blob abc123\tfile1.py"
    assert get_file_exists("abc123", "file1.py", "/path/to/repo") is True


@patch('git_utils.git_commands.run_git_command')
def test_get_file_exists_failure(mock_run_git_command):
    """Test failure in file existence check."""
    mock_run_git_command.side_effect = ValueError("Error message")
    with pytest.raises(ValueError):
        get_file_exists("abc123", "file1.py", "/path/to/repo")


@patch('git_utils.git_commands.get_file_exists')
@patch('git_utils.git_commands.run_git_command')
def test_get_diff_file_exists(mock_run_git_command, mock_get_file_exists):
    """Test successful diff retrieval when files exist."""
    mock_get_file_exists.side_effect = [True, True]
    mock_run_git_command.return_value = "diff output"

    diff = get_diff("abc123", "file1.py", "def456",
                    "file1.py", "/path/to/repo")
    assert diff == "diff output"


@patch('git_utils.git_commands.get_file_exists')
def test_get_diff_file_not_exists(mock_get_file_exists):
    """Test failure in diff retrieval when files do not exist."""
    mock_get_file_exists.side_effect = [False, False]
    with pytest.raises(FileNotFoundError):
        get_diff("abc123", "file1.py", "def456", "file1.py", "/path/to/repo")
