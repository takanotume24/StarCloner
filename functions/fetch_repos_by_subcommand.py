import argparse
from typing import List, Optional
from pytypes.repo_info import RepoInfo
from functions.fetch_starred_repositories import fetch_starred_repositories
from functions.fetch_user_repositories import fetch_user_repositories
from functions.fetch_org_repositories import fetch_org_repositories


def fetch_repos_by_subcommand(
    args: argparse.Namespace, token: Optional[str]
) -> List[RepoInfo]:
    """
    Fetch the repository list based on the subcommand (star, repo, or org).
    """
    match args.command:
        case "star":
            return fetch_starred_repositories(args.username, token)
        case "repo":
            return fetch_user_repositories(
                username=args.username,
                token=token,
                include_forks=args.include_forks,
                include_archived=args.include_archived,
            )
        case "org":
            return fetch_org_repositories(
                orgname=args.orgname,
                token=token,
                include_forks=args.include_forks,
                include_archived=args.include_archived,
            )
        case _:
            # This should never happen if subcommands are required
            return []
