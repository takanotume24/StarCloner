#!/usr/bin/env python3

import argparse
import os
import sys
import requests
import subprocess


def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Clone all repositories starred by a specified GitHub user, with optional star-based filtering."
    )
    parser.add_argument(
        "username",
        help="The GitHub username whose starred repositories should be cloned."
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Dry-run: display which repositories would be cloned without actually cloning."
    )
    parser.add_argument(
        "--min-stars",
        type=int,
        default=None,
        help="Only include repositories with a stargazer count >= this value."
    )
    parser.add_argument(
        "--max-stars",
        type=int,
        default=None,
        help="Only include repositories with a stargazer count <= this value."
    )
    return parser.parse_args()


def fetch_starred_repositories(username, token=None):
    """
    Retrieve data about all repositories starred by the given username.
    Uses the public GitHub API, handling pagination as needed.

    Returns a list of repository data dictionaries, each containing:
    {
        "full_name":        "owner/repo",
        "clone_url":        "https://github.com/owner/repo.git",
        "stargazers_count": 123,
        ...
    }

    token: a personal access token string from the environment (optional).
    """
    all_repos = []
    page = 1
    headers = {}

    if token:
        headers["Authorization"] = f"token {token}"

    while True:
        url = f"https://api.github.com/users/{username}/starred"
        params = {"page": page, "per_page": 100}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(
                f"Error: GitHub API request returned status code {response.status_code}.",
                file=sys.stderr
            )
            break

        data = response.json()
        if not data:
            # No more data; we've reached the end
            break

        all_repos.extend(data)
        page += 1

    return all_repos


def filter_repositories_by_star_count(repos, min_stars=None, max_stars=None):
    """
    Filter the given list of repository data dictionaries based on star count.
    If min_stars is provided, exclude repos with fewer stars.
    If max_stars is provided, exclude repos with more stars.
    """
    filtered = []
    for repo in repos:
        count = repo.get("stargazers_count", 0)

        if min_stars is not None and count < min_stars:
            continue
        if max_stars is not None and count > max_stars:
            continue

        filtered.append(repo)

    return filtered


def confirm_action(repo_count, dry_run=False):
    """
    Display the number of repositories to process and the current mode
    (dry-run or actual cloning), then ask the user to confirm whether to proceed.
    """
    mode = "dry-run (no actual cloning)" if dry_run else "actual cloning"
    print(f"\nYou are about to process {repo_count} repository(ies) with {mode}.")
    choice = input("Proceed? [y/N]: ").strip().lower()
    return choice == 'y'


def clone_repositories(repo_data, target_dir, dry_run=False):
    """
    Clone each repository in the provided repo_data list into the specified target_dir.
    If dry_run is True, no actual cloning will occur; the script will only display what it would do.
    """
    os.makedirs(target_dir, exist_ok=True)

    for repo in repo_data:
        clone_url = repo.get("clone_url")
        full_name = repo.get("full_name", clone_url)  # fallback if full_name is missing

        if dry_run:
            print(f"Dry-run: Would clone {clone_url} into {target_dir}/ (Repository: {full_name})")
        else:
            print(f"Cloning: {clone_url} into {target_dir}/ (Repository: {full_name})")
            subprocess.run(["git", "clone", clone_url], cwd=target_dir, check=False)


def main():
    args = parse_arguments()

    # Get the GitHub token from environment variable (optional)
    token = os.environ.get("GITHUB_TOKEN", None)

    # Fetch all starred repositories for the specified user
    starred = fetch_starred_repositories(args.username, token=token)
    if not starred:
        print(f"No starred repositories found for user '{args.username}', or an error occurred.")
        sys.exit(0)

    # Filter repositories by star count if requested
    filtered = filter_repositories_by_star_count(
        starred,
        min_stars=args.min_stars,
        max_stars=args.max_stars
    )

    if not filtered:
        print("No repositories match the specified star count criteria.")
        sys.exit(0)

    # Sort repos by their full_name in alphabetical order
    filtered.sort(key=lambda r: r.get("full_name", "").lower())

    # Display the filtered repositories
    print(f"Repositories to process (total {len(filtered)}), sorted alphabetically:")
    for repo in filtered:
        name = repo.get("full_name", "unknown/unknown")
        stars = repo.get("stargazers_count", 0)
        print(f"  {name} (Stars: {stars})")

    # Prompt for confirmation
    if not confirm_action(len(filtered), dry_run=args.dry_run):
        print("Process canceled.")
        sys.exit(0)

    # Clone or dry-run
    clone_repositories(filtered, target_dir=args.username, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
