from pathlib import Path
from typing import List
from types.repo_info import RepoInfo
from functions.clone_or_pull_repo import clone_or_pull_repo


def process_repositories(
    repos: List[RepoInfo], target_dir: Path, dry_run: bool
) -> None:
    """
    Clone or pull each repository in the list into the specified directory.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    for repo in repos:
        clone_or_pull_repo(repo, target_dir, dry_run)
