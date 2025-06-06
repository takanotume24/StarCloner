import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments using subcommands: "star", "repo", or "org".
    """
    parser = argparse.ArgumentParser(
        description="Clone or pull GitHub repositories. "
        "Supports cloning starred repositories, user-owned repositories, or organization-owned repositories."
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
        "username", help="The GitHub username whose repositories will be processed."
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

    # --- subcommand: org ---
    org_parser = subparsers.add_parser(
        "org", help="Clone/pull repositories that the organization owns."
    )
    org_parser.add_argument(
        "orgname", help="The GitHub organization whose repositories will be processed."
    )
    org_parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Dry-run: show which repositories would be processed without making changes.",
    )
    org_parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip confirmation prompts and proceed automatically.",
    )
    org_parser.add_argument(
        "--include-forks",
        action="store_true",
        help="Include forked repositories as well.",
    )
    org_parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Include archived repositories as well.",
    )
    org_parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="Directory where the repositories will be cloned. Defaults to current dir.",
    )

    # --- subcommand: maintenance ---
    maintenance_parser = subparsers.add_parser(
        "maintenance", help="Perform maintenance tasks."
    )
    maintenance_subparsers = maintenance_parser.add_subparsers(dest="maintenance_command", required=True)

    # Subcommand reflecting file moving
    move_temp_files_parser = maintenance_subparsers.add_parser(
        "move-temp-files", help="Move temporary files to a designated directory."
    )
    move_temp_files_parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Dry-run: show what files would be moved without making changes.",
    )

    list_cloned_parser = subparsers.add_parser(
        "list-cloned", help="List all cloned repositories in the specified directory."
    )
    list_cloned_parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="Directory where the repositories are cloned. Defaults to current dir.",
    )

    return parser.parse_args()
