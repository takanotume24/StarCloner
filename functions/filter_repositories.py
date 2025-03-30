import argparse
from typing import List
from types.repo_info import RepoInfo
from functions.filter_star_repositories import filter_star_repositories


def filter_repositories(
    args: argparse.Namespace, repos: List[RepoInfo]
) -> List[RepoInfo]:
    """
    Apply filtering based on the subcommand:
      - star: use min_stars / max_stars / owner_filter
      - repo / org: no additional filters needed (forks/archived are handled at fetch time).
    """
    if args.command == "star":
        return filter_star_repositories(
            repos,
            min_stars=args.min_stars,
            max_stars=args.max_stars,
            owner_filter=args.owner_filter,
        )
    else:
        return repos
