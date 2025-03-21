import pytest
from unittest.mock import patch, MagicMock
from git_utils.git_commands import get_merge_base


# Test successful merge base retrieval
@patch('subprocess.run')
def test_get_merge_base_success(mock_run):
    mock_run.return_value = MagicMock(returncode=0,
                                      stdou='abc123',
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
    mock_run.return_value = MagicMock(
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
