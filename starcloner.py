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
    Holds information about a GitHub repository starred by a user.
    """

    full_name: str
    clone_url: str
    stargazers_count: int
    owner_name: str


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Clone (or pull if already exists) all repositories starred by a specified GitHub user, "
        "optionally filtered by star counts and owner name."
    )
    parser.add_argument(
        "username",
        help="The GitHub username whose starred repositories will be processed.",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Dry-run: show which repositories would be processed without making changes.",
    )
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip confirmation prompts and proceed automatically.",
    )
    parser.add_argument(
        "--min-stars",
        type=int,
        default=None,
        help="Only include repositories with stargazer count >= this value.",
    )
    parser.add_argument(
        "--max-stars",
        type=int,
        default=None,
        help="Only include repositories with stargazer count <= this value.",
    )
    parser.add_argument(
        "--owner-filter",
        default=None,
        help="Only include repositories whose owner's name matches this value (case-insensitive).",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="Directory where the starred repositories will be cloned. Defaults to the current working directory.",
    )
    return parser.parse_args()


def fetch_starred_repositories(username: str, token: Optional[str]) -> List[RepoInfo]:
    """
    Fetch all repositories starred by the given user.
    Handles pagination as needed.

    Returns:
        List[RepoInfo] objects containing information about starred repos.
    """
    all_repos: List[RepoInfo] = []
    page: int = 1
    headers: Dict[str, str] = {"Accept": "application/vnd.github.v3+json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"  # Recommended GitHub Auth approach

    while True:
        url = f"https://api.github.com/users/{username}/starred"
        params = {"page": page, "per_page": 100}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(
                f"Error: GitHub API request returned status code {response.status_code}.",
                file=sys.stderr,
            )
            print("Response body:", response.text, file=sys.stderr)
            break

        data = response.json()
        if not data:
            # No more data; reached the end of pages.
            break

        # Convert each repository dict from the API into a RepoInfo dataclass instance
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


def filter_repositories(
    repos: List[RepoInfo],
    min_stars: Optional[int],
    max_stars: Optional[int],
    owner_filter: Optional[str],
) -> List[RepoInfo]:
    """
    Filter the list of repositories based on stargazer count and owner's name.
    """
    filtered = []
    for repo in repos:
        # Filter by star count
        if min_stars is not None and repo.stargazers_count < min_stars:
            continue
        if max_stars is not None and repo.stargazers_count > max_stars:
            continue

        # Filter by owner's name
        if owner_filter is not None:
            if repo.owner_name.lower() != owner_filter.lower():
                continue

        filtered.append(repo)

    return filtered


def confirm_action(repo_count: int, dry_run: bool) -> bool:
    """
    Ask for user confirmation before proceeding, unless in dry-run or auto-confirm mode.
    """
    mode = "dry-run (no changes will be made)" if dry_run else "actual clone/pull"
    print(f"\nYou are about to process {repo_count} repository(ies) with {mode}.")
    choice = input("Proceed? [y/N]: ").strip().lower()
    return choice == "y"


def clone_or_pull_repo(repo: RepoInfo, target_dir: Path, dry_run: bool) -> None:
    """
    Clone or pull a repository into target_dir:
      - If the directory doesn't exist, perform clone.
      - If it exists, run 'git pull'.
    """
    clone_url = repo.clone_url
    full_name = repo.full_name

    # Use the last part of "owner/repo" as the local folder name (e.g., "repo").
    local_repo_dir_name = full_name.split("/")[-1]
    local_path = target_dir / local_repo_dir_name

    if local_path.is_dir():
        # Repository already cloned; perform pull
        if dry_run:
            print(f"Dry-run: Would pull in '{local_path}' (Repository: {full_name})")
        else:
            print(f"Pulling in '{local_path}' (Repository: {full_name})")
            subprocess.run(["git", "-C", str(local_path), "pull"], check=False)
    else:
        # Repository not cloned; perform clone
        if dry_run:
            print(
                f"Dry-run: Would clone {clone_url} into '{target_dir}' (Repository: {full_name})"
            )
        else:
            print(f"Cloning: {clone_url} into '{target_dir}' (Repository: {full_name})")
            subprocess.run(
                ["git", "clone", clone_url], cwd=str(target_dir), check=False
            )


def process_repositories(
    repo_data: List[RepoInfo], target_dir: Path, dry_run: bool
) -> None:
    """
    Process each repository: if the local directory exists, pull updates; otherwise, clone it.
    """
    target_dir.mkdir(parents=True, exist_ok=True)

    for repo in repo_data:
        clone_or_pull_repo(repo, target_dir, dry_run)


def main() -> None:
    args = parse_arguments()

    # Determine the final path (use --output-dir directly)
    parent_dir = Path(args.output_dir).resolve()
    final_path = parent_dir

    # Read token from environment variable
    token = os.environ.get("GITHUB_TOKEN", None)

    if token:
        print("Authentication token loaded from environment variable.")
    else:
        print("No authentication token provided. Proceeding without authentication.")

    # Fetch all repositories starred by the specified user
    starred_repos = fetch_starred_repositories(args.username, token)
    if not starred_repos:
        print(
            f"No starred repositories found for user '{args.username}' or an error occurred."
        )
        sys.exit(0)

    # Filter repositories by stargazer count and owner's name (if specified)
    filtered_repos = filter_repositories(
        starred_repos,
        min_stars=args.min_stars,
        max_stars=args.max_stars,
        owner_filter=args.owner_filter,
    )

    if not filtered_repos:
        print("No repositories match the specified criteria.")
        sys.exit(0)

    # Sort repositories alphabetically by full_name
    filtered_repos.sort(key=lambda r: r.full_name.lower())

    # Display the filtered repositories
    print(
        f"Repositories to process (total {len(filtered_repos)}), sorted alphabetically:"
    )
    for repo in filtered_repos:
        print(
            f"  {repo.full_name} (Stars: {repo.stargazers_count}, Owner: {repo.owner_name})"
        )

    # If '--yes' is not specified, prompt for confirmation
    if not args.yes:
        if not confirm_action(len(filtered_repos), args.dry_run):
            print("Process canceled.")
            sys.exit(0)
    else:
        print("\n'--yes' specified; skipping confirmation prompt.\n")

    # Clone or pull repositories
    process_repositories(filtered_repos, target_dir=final_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
