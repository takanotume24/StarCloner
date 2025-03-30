from typing import List
from pytypes.repo_info import RepoInfo


def print_repositories(repos: List[RepoInfo]) -> None:
    """
    Print a sorted list of repositories, showing metadata like stargazer count and owner.
    """
    repos_sorted = sorted(repos, key=lambda r: r.full_name.lower())
    print(
        f"Repositories to process (total {len(repos_sorted)}), sorted alphabetically:"
    )
    for repo in repos_sorted:
        print(
            f"  {repo.full_name} (Stars: {repo.stargazers_count}, "
            f"Owner: {repo.owner_name})"
        )
