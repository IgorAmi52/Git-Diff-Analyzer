import pytest
from unittest.mock import patch, MagicMock

from git_diff_analyzer.services.diff_service import compare_local_remote_changes, _get_filtered_changed_files


def test_get_filtered_changed_files():
    # Setup
    base_commit = 'abc123'
    changed_files = ['file1.txt', 'file2.txt', 'file3.txt']
    latest_commit = 'def456'

    # Mock diff function that returns True for file1.txt and file3.txt
    def mock_diff_func(base, file, latest, _):
        if file == 'file2.txt':
            return False  # No real changes
        if file == 'file3.txt':
            raise FileNotFoundError("Test file not found")
        return True  # For file1.txt

    # Call function
    filtered_files = _get_filtered_changed_files(
        base_commit, changed_files, latest_commit, mock_diff_func
    )

    # Assertions
    assert 'file1.txt' in filtered_files
    assert 'file2.txt' not in filtered_files
    assert 'file3.txt' in filtered_files
    assert len(filtered_files) == 2


def test_get_filtered_changed_files_with_value_error():
    # Setup
    base_commit = 'abc123'
    changed_files = ['file1.txt', 'error_file.txt']
    latest_commit = 'def456'

    # Mock diff function that raises ValueError for error_file.txt
    def mock_diff_func(base, file, latest, _):
        if file == 'error_file.txt':
            raise ValueError("Test error")
        return True

    # Call function
    with patch('logging.Logger.warning') as mock_warning:
        filtered_files = _get_filtered_changed_files(
            base_commit, changed_files, latest_commit, mock_diff_func
        )

    # Assertions
    assert 'file1.txt' in filtered_files
    assert 'error_file.txt' not in filtered_files
    assert len(filtered_files) == 1
    mock_warning.assert_called_once()


@patch('git_diff_analyzer.remote.remote_interface.RemoteInterface.get_latest_commit')
@patch('git_diff_analyzer.services.repo_mapper.get_remote_service')
@patch('git_diff_analyzer.git_utils.git_commands.get_merge_base')
def test_compare_local_remote_changes_remote_error(
    mock_get_merge_base,  # First parameter corresponds to last decorator
    mock_get_remote_service,  # Second parameter corresponds to middle decorator
    mock_get_latest_commit  # Third parameter corresponds to first decorator
):
    # Set up the merge base mock
    mock_get_merge_base.return_value = "test-base-commit"

    # Create a mock remote service that will be returned
    mock_remote = MagicMock()
    mock_remote.get_latest_commit = mock_get_latest_commit  # Connect the mock method
    mock_get_remote_service.return_value = mock_remote

    # Set up the error
    mock_get_latest_commit.side_effect = ValueError("Test error")

    # Test that the error is raised
    with pytest.raises(ValueError):
        compare_local_remote_changes(
            'test-owner', 'test-repo', 'fake-token-123', '/path/to/local/repo', 'main', 'feature-branch')
