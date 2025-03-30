#!/usr/bin/env python3

import argparse
import os
import sys
import requests
import subprocess
from typing import Any, Dict, List, Optional


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Clone (or pull if already exists) all repositories starred by a specified GitHub user, with optional star-based filtering."
    )
    parser.add_argument(
        "username",
        help="The GitHub username whose starred repositories should be cloned/pulled.",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Dry-run: display which repositories would be processed without actually doing it.",
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
        help="Only include repositories with a stargazer count >= this value.",
    )
    parser.add_argument(
        "--max-stars",
        type=int,
        default=None,
        help="Only include repositories with a stargazer count <= this value.",
    )
    return parser.parse_args()


def fetch_starred_repositories(
    username: str, token: Optional[str]
) -> List[Dict[str, Any]]:
    """
    Retrieve data about all repositories starred by the given username.
    Uses the public GitHub API, handling pagination as needed.

    Returns a list of repository data dictionaries, each containing fields like:
    {
        "full_name":        "owner/repo",
        "clone_url":        "https://github.com/owner/repo.git",
        "stargazers_count": 123,
        ...
    }

    :param username: GitHub username to fetch starred repositories for.
    :param token: GitHub personal access token string (can be None).
    :return: A list of dictionaries representing the starred repositories.
    """
    all_repos: List[Dict[str, Any]] = []
    page: int = 1
    headers: Dict[str, str] = {}

    if token:
        headers["Authorization"] = f"token {token}"

    while True:
        url = f"https://api.github.com/users/{username}/starred"
        params = {"page": page, "per_page": 100}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(
                f"Error: GitHub API request returned status code {response.status_code}.",
                file=sys.stderr,
            )
            break

        data = response.json()
        if not data:
            # No more data; we've reached the end
            break

        all_repos.extend(data)
        page += 1

    return all_repos


def filter_repositories_by_star_count(
    repos: List[Dict[str, Any]], min_stars: Optional[int], max_stars: Optional[int]
) -> List[Dict[str, Any]]:
    """
    Filter the given list of repository data dictionaries based on star count.

    :param repos: List of repository data dictionaries.
    :param min_stars: If not None, exclude repos with fewer stars.
    :param max_stars: If not None, exclude repos with more stars.
    :return: A list of filtered repository data dictionaries.
    """
    filtered: List[Dict[str, Any]] = []
    for repo in repos:
        count = repo.get("stargazers_count", 0)

        if min_stars is not None and count < min_stars:
            continue
        if max_stars is not None and count > max_stars:
            continue

        filtered.append(repo)

    return filtered


def confirm_action(repo_count: int, dry_run: bool) -> bool:
    """
    Display the number of repositories to process and the current mode
    (dry-run or actual cloning/pulling), then ask the user to confirm whether to proceed.

    :param repo_count: Number of repositories to be processed.
    :param dry_run: Whether the operation is a dry-run or not.
    :return: True if user confirms to proceed, False otherwise.
    """
    mode: str = "dry-run (no actual changes)" if dry_run else "actual clone/pull"
    print(f"\nYou are about to process {repo_count} repository(ies) with {mode}.")
    choice: str = input("Proceed? [y/N]: ").strip().lower()
    return choice == "y"


def clone_or_pull_repo(repo: Dict[str, Any], target_dir: str, dry_run: bool) -> None:
    """
    Clone or pull a single repository:
      - If the directory doesn't exist, clone.
      - If it exists, run 'git pull'.
    """
    clone_url = repo.get("clone_url")
    full_name = repo.get("full_name", clone_url)  # fallback if full_name is missing

    # Use the last part of the "owner/repo" name as the folder name
    local_repo_dir_name = full_name.split("/")[-1]  # e.g., "repo"
    local_path = os.path.join(target_dir, local_repo_dir_name)

    if os.path.isdir(local_path):
        # Already cloned; do pull
        if dry_run:
            print(f"Dry-run: Would pull in '{local_path}' (Repository: {full_name})")
        else:
            print(f"Pulling in '{local_path}' (Repository: {full_name})")
            subprocess.run(["git", "-C", local_path, "pull"], check=False)
    else:
        # Need to clone
        if dry_run:
            print(f"Dry-run: Would clone {clone_url} into {target_dir}/ (Repository: {full_name})")
        else:
            print(f"Cloning: {clone_url} into {target_dir}/ (Repository: {full_name})")
            subprocess.run(["git", "clone", clone_url], cwd=target_dir, check=False)


def process_repositories(
    repo_data: List[Dict[str, Any]], target_dir: str, dry_run: bool
) -> None:
    """
    For each repository in repo_data:
      - Check if local directory exists and decide whether to clone or pull.
    """
    os.makedirs(target_dir, exist_ok=True)

    for repo in repo_data:
        clone_or_pull_repo(repo, target_dir, dry_run)


def main() -> None:
    args: argparse.Namespace = parse_arguments()

    # Get the GitHub token from environment variable (optional)
    token: Optional[str] = os.environ.get("GITHUB_TOKEN", None)

    # Fetch all starred repositories for the specified user
    starred: List[Dict[str, Any]] = fetch_starred_repositories(args.username, token)
    if not starred:
        print(
            f"No starred repositories found for user '{args.username}', or an error occurred."
        )
        sys.exit(0)

    # Filter repositories by star count if requested
    filtered: List[Dict[str, Any]] = filter_repositories_by_star_count(
        starred, args.min_stars, args.max_stars
    )

    if not filtered:
        print("No repositories match the specified star count criteria.")
        sys.exit(0)

    # Sort repos by their full_name in alphabetical order
    filtered.sort(key=lambda r: r.get("full_name", "").lower())

    # Display the filtered repositories
    print(f"Repositories to process (total {len(filtered)}), sorted alphabetically:")
    for repo in filtered:
        name: str = repo.get("full_name", "unknown/unknown")
        stars: int = repo.get("stargazers_count", 0)
        print(f"  {name} (Stars: {stars})")

    # If not in 'yes' mode, prompt for confirmation
    if not args.yes:
        if not confirm_action(len(filtered), args.dry_run):
            print("Process canceled.")
            sys.exit(0)
    else:
        print("\n'--yes' specified; skipping confirmation prompt.\n")

    # Clone or pull
    process_repositories(filtered, target_dir=args.username, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
