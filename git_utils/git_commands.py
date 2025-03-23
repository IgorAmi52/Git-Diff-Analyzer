import logging
import subprocess
from typing import List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run_git_command(command: List[str], repo_loc: str) -> str:
    """Helper function to run a git command and handle errors."""
    try:
        result = subprocess.run(command, cwd=repo_loc,
                                capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Error in git command: {command}, {result.stderr}")
            raise ValueError(f"Git command failed: {result.stderr.strip()}")
        return result.stdout.strip()
    except Exception as e:
        logger.error(
            f"Unexpected error while running git command {command}: {e}")
        raise ValueError(f"Unexpected error: {e}")


def get_merge_base(branch_a, branch_b, repo_loc):
    """Find the last common commit (merge base) between two branches."""
    try:
        return run_git_command(['git', 'merge-base', branch_a, branch_b], repo_loc)
    except ValueError as e:
        logger.error(
            f"Failed to get merge base for branches {branch_a} and {branch_b}: {e}")
        raise ValueError(f"Failed to get merge base: {e}")


def get_local_last_commit(branch, repo_loc):
    """Get the last commit hash in the local branch."""
    try:
        return run_git_command(['git', 'rev-parse', f"refs/heads/{branch}"], repo_loc)
    except ValueError as e:
        logger.error(f"Failed to get the last commit for branch {branch}: {e}")
        raise ValueError(f"Failed to get last commit: {e}")


def get_changed_files(repo_loc, base_commit_hash, commit_hash):
    """Get a list of changed files between two commits."""
    try:
        output = run_git_command(
            ['git', 'diff', '--name-only', f'{base_commit_hash}..{commit_hash}'], repo_loc)
        return output.split('\n')
    except ValueError as e:
        logger.error(
            f"Failed to get changed files between {base_commit_hash} and {commit_hash}: {e}")
        raise ValueError(f"Failed to get changed files: {e}")


def get_file_exists(commit, file_path, repo_loc):
    """Check if the file exists in a given commit."""
    try:
        output = run_git_command(
            ['git', 'ls-tree', commit, file_path], repo_loc)
        return output != ''
    except ValueError as e:
        logger.error(
            f"Failed to check if file {file_path} exists in commit {commit}: {e}")
        raise ValueError(f"Failed to check file existence: {e}")


def get_diff(commit_a, file_ca, commit_b, file_cb, repo_loc):
    """Get the diff between two files in two different commits."""
    try:
        # Check if files exist in both commits
        if not get_file_exists(commit_a, file_ca, repo_loc):
            raise FileNotFoundError(
                f"File '{file_ca}' not found in commit {commit_a}.")
        if not get_file_exists(commit_b, file_cb, repo_loc):
            raise FileNotFoundError(
                f"File '{file_cb}' not found in commit {commit_b}.")

        # If both files exist, proceed to get the diff
        return run_git_command(['git', 'diff', f'{commit_a}:{file_ca}', f'{commit_b}:{file_cb}'], repo_loc)
    except FileNotFoundError:
        raise
    except ValueError as e:
        logger.error(
            f"Failed to get diff for files {file_ca} and {file_cb} between commits {commit_a} and {commit_b}: {e}")
        raise ValueError(f"Failed to get diff: {e}")
