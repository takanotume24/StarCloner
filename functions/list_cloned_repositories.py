from pathlib import Path
from pytypes.repo_info import RepoInfo
from functions.print_repositories import print_repositories

def list_cloned_repositories(target_dir: Path) -> None:
    """
    List all cloned repositories in the target directory.
    """
    cloned_repos = []
    for user_dir in target_dir.iterdir():
        if user_dir.is_dir():
            for repo_dir in user_dir.iterdir():
                if repo_dir.is_dir():
                    repo_info = RepoInfo(
                        full_name=f"{user_dir.name}/{repo_dir.name}",
                        clone_url="",  # Not needed for listing
                        stargazers_count=0,  # Not needed for listing
                        owner_name=user_dir.name
                    )
                    cloned_repos.append(repo_info)
    print_repositories(cloned_repos)
