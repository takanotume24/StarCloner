#!/usr/bin/env python3

import argparse
import os
import sys
import requests
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class RepoInfo:
    """
    Holds information about a GitHub repository.
    """

    full_name: str
    clone_url: str
    stargazers_count: int
    owner_name: str


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments using subcommands: "star" or "repo".
    """
    parser = argparse.ArgumentParser(
        description="Clone or pull GitHub repositories. "
        "Supports cloning starred repositories or user-owned repositories."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- subcommand: star ---
    star_parser = subparsers.add_parser(
        "star", help="Clone/pull repositories that the user has starred."
    )
    star_parser.add_argument(
        "username",
        help="The GitHub username whose starred repositories will be processed.",
    )
    star_parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Dry-run: show which repositories would be processed without making changes.",
    )
    star_parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip confirmation prompts and proceed automatically.",
    )
    star_parser.add_argument(
        "--min-stars",
        type=int,
        default=None,
        help="Only include repositories with stargazer count >= this value.",
    )
    star_parser.add_argument(
        "--max-stars",
        type=int,
        default=None,
        help="Only include repositories with stargazer count <= this value.",
    )
    star_parser.add_argument(
        "--owner-filter",
        default=None,
        help="Only include repositories whose owner's name matches this (case-insensitive).",
    )
    star_parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="Directory where the repositories will be cloned. Defaults to current dir.",
    )

    # --- subcommand: repo ---
    repo_parser = subparsers.add_parser(
        "repo", help="Clone/pull repositories that the user owns."
    )
    repo_parser.add_argument(
        "username", help="The GitHub username whose own repositories will be processed."
    )
    repo_parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Dry-run: show which repositories would be processed without making changes.",
    )
    repo_parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip confirmation prompts and proceed automatically.",
    )
    repo_parser.add_argument(
        "--include-forks",
        action="store_true",
        help="Include forked repositories as well.",
    )
    repo_parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Include archived repositories as well.",
    )
    repo_parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="Directory where the repositories will be cloned. Defaults to current dir.",
    )

    return parser.parse_args()


def fetch_starred_repositories(username: str, token: Optional[str]) -> List[RepoInfo]:
    """
    Fetch all repositories starred by the given user (via GitHub API).
    """
    all_repos: List[RepoInfo] = []
    page: int = 1
    headers: Dict[str, str] = {"Accept": "application/vnd.github.v3+json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    while True:
        url = f"https://api.github.com/users/{username}/starred"
        params = {"page": page, "per_page": 100}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(
                f"Error: GitHub API request returned {response.status_code}.",
                file=sys.stderr,
            )
            print("Response body:", response.text, file=sys.stderr)
            break

        data = response.json()
        if not data:
            break  # No more data

        for item in data:
            repo_info = RepoInfo(
                full_name=item["full_name"],
                clone_url=item["clone_url"],
                stargazers_count=item["stargazers_count"],
                owner_name=item["owner"]["login"],
            )
            all_repos.append(repo_info)

        page += 1

    return all_repos


def fetch_user_repositories(
    username: str, token: Optional[str], include_forks: bool, include_archived: bool
) -> List[RepoInfo]:
    """
    Fetch all repositories owned by the given user (via GitHub API).
    Optionally include forked or archived repositories.
    """
    all_repos: List[RepoInfo] = []
    page: int = 1
    headers: Dict[str, str] = {"Accept": "application/vnd.github.v3+json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    while True:
        url = f"https://api.github.com/users/{username}/repos"
        params = {
            "page": page,
            "per_page": 100,
            "type": "all",  # 'all' includes private, forks, etc., if authorized
            "sort": "full_name",
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(
                f"Error: GitHub API request returned {response.status_code}.",
                file=sys.stderr,
            )
            print("Response body:", response.text, file=sys.stderr)
            break

        data = response.json()
        if not data:
            break

        for item in data:
            # Skip forks unless --include-forks
            if not include_forks and item["fork"]:
                continue
            # Skip archived unless --include-archived
            if not include_archived and item["archived"]:
                continue

            repo_info = RepoInfo(
                full_name=item["full_name"],
                clone_url=item["clone_url"],
                stargazers_count=item["stargazers_count"],
                owner_name=item["owner"]["login"],
            )
            all_repos.append(repo_info)

        page += 1

    return all_repos


def filter_repositories(
    repos: List[RepoInfo],
    min_stars: Optional[int],
    max_stars: Optional[int],
    owner_filter: Optional[str],
) -> List[RepoInfo]:
    """
    Filter the list of repositories based on stargazer count and owner's name.
    (Used mainly for 'star' subcommand.)
    """
    filtered = []
    for repo in repos:
        if min_stars is not None and repo.stargazers_count < min_stars:
            continue
        if max_stars is not None and repo.stargazers_count > max_stars:
            continue
        if owner_filter is not None:
            if repo.owner_name.lower() != owner_filter.lower():
                continue
        filtered.append(repo)
    return filtered


def confirm_action(repo_count: int, dry_run: bool) -> bool:
    """
    Ask user to confirm before proceeding, unless in dry-run or --yes mode.
    """
    mode = "dry-run (no changes)" if dry_run else "actual clone/pull"
    print(f"\nYou are about to process {repo_count} repository(ies) with {mode}.")
    choice = input("Proceed? [y/N]: ").strip().lower()
    return choice == "y"


def clone_or_pull_repo(repo: RepoInfo, target_dir: Path, dry_run: bool) -> None:
    """
    Clone or pull a repository into target_dir:
      - If the directory doesn't exist, do clone.
      - If it exists, run 'git pull'.
    """
    local_repo_dir_name = repo.full_name.split("/")[-1]
    local_path = target_dir / local_repo_dir_name

    if local_path.is_dir():
        if dry_run:
            print(
                f"Dry-run: Would pull in '{local_path}' (Repository: {repo.full_name})"
            )
        else:
            print(f"Pulling in '{local_path}' (Repository: {repo.full_name})")
            subprocess.run(["git", "-C", str(local_path), "pull"], check=False)
    else:
        if dry_run:
            print(
                f"Dry-run: Would clone {repo.clone_url} into '{target_dir}' "
                f"(Repository: {repo.full_name})"
            )
        else:
            print(
                f"Cloning {repo.clone_url} into '{target_dir}' "
                f"(Repository: {repo.full_name})"
            )
            subprocess.run(
                ["git", "clone", repo.clone_url], cwd=str(target_dir), check=False
            )


def process_repositories(
    repo_data: List[RepoInfo], target_dir: Path, dry_run: bool
) -> None:
    """
    Clone or pull each repo in repo_data into target_dir.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    for repo in repo_data:
        clone_or_pull_repo(repo, target_dir, dry_run)


def main() -> None:
    args = parse_arguments()

    # Read GitHub token from environment (if any)
    token = os.environ.get("GITHUB_TOKEN", None)
    if token:
        print("Authentication token loaded from environment variable.")
    else:
        print("No authentication token found. Proceeding without authentication.")

    if args.command == "star":
        # --- star subcommand ---
        starred_repos = fetch_starred_repositories(args.username, token)
        if not starred_repos:
            print(
                f"No starred repositories found for user '{args.username}' "
                "or an error occurred."
            )
            sys.exit(0)

        filtered_repos = filter_repositories(
            starred_repos,
            min_stars=args.min_stars,
            max_stars=args.max_stars,
            owner_filter=args.owner_filter,
        )

        if not filtered_repos:
            print("No repositories match the specified criteria.")
            sys.exit(0)

        filtered_repos.sort(key=lambda r: r.full_name.lower())
        print(
            f"Repositories to process (total {len(filtered_repos)}), "
            "sorted alphabetically:"
        )
        for repo in filtered_repos:
            print(
                f"  {repo.full_name} (Stars: {repo.stargazers_count}, "
                f"Owner: {repo.owner_name})"
            )

        if not args.yes:
            if not confirm_action(len(filtered_repos), args.dry_run):
                print("Process canceled.")
                sys.exit(0)
        else:
            print("\n'--yes' specified; skipping confirmation prompt.\n")

        process_repositories(
            filtered_repos,
            target_dir=Path(args.output_dir).resolve(),
            dry_run=args.dry_run,
        )

    elif args.command == "repo":
        # --- repo subcommand ---
        user_repos = fetch_user_repositories(
            username=args.username,
            token=token,
            include_forks=args.include_forks,
            include_archived=args.include_archived,
        )
        if not user_repos:
            print(
                f"No user repositories found for '{args.username}' "
                "or an error occurred."
            )
            sys.exit(0)

        user_repos.sort(key=lambda r: r.full_name.lower())
        print(
            f"Repositories to process (total {len(user_repos)}), sorted alphabetically:"
        )
        for repo in user_repos:
            print(
                f"  {repo.full_name} (Stars: {repo.stargazers_count}, "
                f"Owner: {repo.owner_name})"
            )

        if not args.yes:
            if not confirm_action(len(user_repos), args.dry_run):
                print("Process canceled.")
                sys.exit(0)
        else:
            print("\n'--yes' specified; skipping confirmation prompt.\n")

        process_repositories(
            user_repos, target_dir=Path(args.output_dir).resolve(), dry_run=args.dry_run
        )

    else:
        # Should never happen if 'dest="command", required=True' is set
        print("Unknown command.")
        sys.exit(1)


if __name__ == "__main__":
    main()
