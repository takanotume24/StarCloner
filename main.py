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
        description="Clone all repositories starred by a specified GitHub user, with optional star-based filtering."
    )
    parser.add_argument(
        "username",
        help="The GitHub username whose starred repositories should be cloned.",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Dry-run: display which repositories would be cloned without actually cloning.",
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
    (dry-run or actual cloning), then ask the user to confirm whether to proceed.

    :param repo_count: Number of repositories to be processed.
    :param dry_run: Whether the operation is a dry-run or not.
    :return: True if user confirms to proceed, False otherwise.
    """
    mode: str = "dry-run (no actual cloning)" if dry_run else "actual cloning"
    print(f"\nYou are about to process {repo_count} repository(ies) with {mode}.")
    choice: str = input("Proceed? [y/N]: ").strip().lower()
    return choice == "y"


def clone_repositories(
    repo_data: List[Dict[str, Any]], target_dir: str, dry_run: bool
) -> None:
    """
    Clone each repository in the provided repo_data list into the specified target_dir.
    If dry_run is True, no actual cloning will occur; the script will only display what it would do.

    :param repo_data: List of repository data dictionaries to clone.
    :param target_dir: The directory path under which to clone repositories.
    :param dry_run: Whether to actually clone or just simulate.
    """
    os.makedirs(target_dir, exist_ok=True)

    for repo in repo_data:
        clone_url = repo.get("clone_url")
        full_name = repo.get("full_name", clone_url)  # fallback if full_name is missing

        if dry_run:
            print(
                f"Dry-run: Would clone {clone_url} into {target_dir}/ (Repository: {full_name})"
            )
        else:
            print(f"Cloning: {clone_url} into {target_dir}/ (Repository: {full_name})")
            subprocess.run(["git", "clone", clone_url], cwd=target_dir, check=False)


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

    # Prompt for confirmation
    if not confirm_action(len(filtered), args.dry_run):
        print("Process canceled.")
        sys.exit(0)

    # Clone or dry-run
    clone_repositories(filtered, target_dir=args.username, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
