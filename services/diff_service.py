from git_utils.git_commands import *
from services.repo_mapper import get_remote_service


def compare_local_remote_changes(owner, repo,
                                 access_token,
                                 local_repo_path,
                                 branch_a,
                                 branch_b):
    base_commit = get_merge_base(
        branch_a, branch_b, local_repo_path)

    # Get the appropriate remote service
    remote_service = get_remote_service('github')
    try:
        remote = remote_service(owner, repo, access_token)
        remote_latest_commit = remote.get_latest_commit(branch_a)
    except ValueError as e:
        print(e)
        return

    local_latest_commit = get_local_last_commit(branch_b, local_repo_path)
