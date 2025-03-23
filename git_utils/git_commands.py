import subprocess


def get_merge_base(branch_a, branch_b, repo_loc):
    """Find the last common commit (merge base) between two branches."""
    results = subprocess.run(['git', 'merge-base', branch_a, branch_b],
                             cwd=repo_loc, capture_output=True, text=True)
    if results.returncode != 0:
        raise ValueError('Error in getting merge base: ' + results.stderr)
    return results.stdout.strip()


def get_local_last_commit(branch, repo_loc):
    """Get the last commit hash in the local branch."""
    result = subprocess.run(['git', 'rev-parse', f"refs/heads/{branch}"],
                            cwd=repo_loc, capture_output=True, text=True)
    if result.returncode != 0:
        raise ValueError(
            f"Error retrieving last commit: {result.stderr.strip()}")

    return result.stdout.strip()


def get_changed_files(repo_loc, base_commit_hash, commit_hash):
    """Get a list of changed files between two commits."""
    results = subprocess.run(['git', 'diff', '--name-only', f'{base_commit_hash}..{commit_hash}'],
                             cwd=repo_loc, capture_output=True, text=True)
    if results.returncode != 0:
        raise ValueError('Error retrieving changed files: ' + results.stderr)
    return results.stdout.strip().split('\n')
