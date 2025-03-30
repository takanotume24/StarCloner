def confirm_action(repo_count: int, dry_run: bool) -> bool:
    """
    Ask the user for confirmation unless --dry-run or --yes is specified.
    """
    mode = "dry-run (no changes)" if dry_run else "actual clone/pull"
    print(f"\nYou are about to process {repo_count} repository(ies) with {mode}.")
    choice = input("Proceed? [y/N]: ").strip().lower()
    return choice == "y"
