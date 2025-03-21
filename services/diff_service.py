import git_utils.git_commands as git_commands


def compare_local_remote_changes(owner, repo,
                                 access_token,
                                 local_repo_path,
                                 branch_a,
                                 branch_b):
    base_commit = git_commands.get_merge_base(branch_a, branch_b, local_repo_path)
    print(base_commit)
