import logging
from git_utils.git_commands import *
from services.repo_mapper import get_remote_service

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def compare_local_remote_changes(owner, repo, access_token, local_repo_path, branch_a, branch_b):
    """Find files that were changed in both local and remote branches since the merge base."""

    # Get merge base commit
    base_commit = get_merge_base(branch_a, branch_b, local_repo_path)

    # Get the remote service
    remote_service = get_remote_service('github')
    try:
        remote = remote_service(owner, repo, access_token)
        remote_latest_commit = remote.get_latest_commit(branch_a)
    except ValueError as e:
        logger.error(f"Remote service error: {e}")
        raise

    # Get changed files remotely
    remote_changed_files = remote.get_changed_files(
        base_commit, remote_latest_commit)

    remote_filtered_files = _get_filtered_changed_files(
        base_commit, remote_changed_files, remote_latest_commit, remote.is_diff
    )
    # Get changed files locally
    local_latest_commit = get_local_last_commit(branch_b, local_repo_path)
    local_changed_files = get_changed_files(
        local_repo_path, base_commit, local_latest_commit)
    local_filtered_files = _get_filtered_changed_files(
        base_commit, local_changed_files, local_latest_commit,
        lambda base, file, latest, _: get_diff(
            base, file, latest, file, local_repo_path)
    )

    # Find common changed files
    return [file for file in remote_filtered_files if file in local_filtered_files]


def _get_filtered_changed_files(base_commit, changed_files, latest_commit, diff_func):
    """Helper function to filter files that have actual differences."""
    filtered_files = []
    for file in changed_files:
        try:
            if diff_func(base_commit, file, latest_commit, file):
                filtered_files.append(file)
        except FileNotFoundError:
            # File is new or removed, still considered a change
            filtered_files.append(file)
        except ValueError as e:
            logger.warning(f"Error processing {file}: {e}")
            continue
    return filtered_files
