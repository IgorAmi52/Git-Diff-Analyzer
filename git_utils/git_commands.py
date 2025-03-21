import subprocess


def get_merge_base(branch_a, branch_b, repo_loc):
    results = subprocess.run(['git', 'merge-base', branch_a, branch_b],
                             cwd=repo_loc, capture_output=True, text=True)
    if results.returncode != 0:
        raise ValueError('Error in getting merge base: ' + results.stderr)
    return results.stdout.strip()
