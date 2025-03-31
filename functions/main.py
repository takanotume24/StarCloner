import os
import sys
from pathlib import Path
from functions.parse_arguments import parse_arguments
from functions.fetch_repos_by_subcommand import fetch_repos_by_subcommand
from functions.filter_repositories import filter_repositories
from functions.print_repositories import print_repositories
from functions.confirm_action import confirm_action
from functions.process_repositories import process_repositories
from pytypes.repo_info import RepoInfo
from functions.list_cloned_repositories import list_cloned_repositories


def main() -> None:
    args = parse_arguments()

    # Read GitHub token from environment (if present)
    token = os.environ.get("GITHUB_TOKEN", None)
    if token:
        print("Authentication token loaded from environment variable.")
    else:
        print("No authentication token found. Proceeding without authentication.")

    if args.command == "list-cloned":
        list_cloned_repositories(Path(args.output_dir).resolve())
        sys.exit(0)

    all_repos = fetch_repos_by_subcommand(args, token)
    if not all_repos:
        print("No repositories found or an error occurred.")
        sys.exit(0)

    # 2) Filter repositories
    filtered_repos = filter_repositories(args, all_repos)
    if not filtered_repos:
        print("No repositories match the specified criteria.")
        sys.exit(0)

    # 3) Print repository list
    print_repositories(filtered_repos)

    # 4) Confirm action unless --yes is specified
    if not args.yes:
        if not confirm_action(len(filtered_repos), args.dry_run):
            print("Process canceled.")
            sys.exit(0)
    else:
        print("\n'--yes' specified; skipping confirmation prompt.\n")

    # 5) Perform clone or pull operations
    process_repositories(
        filtered_repos, target_dir=Path(args.output_dir).resolve(), dry_run=args.dry_run
    )
