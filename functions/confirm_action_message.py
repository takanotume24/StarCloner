def confirm_action_message(repo_count: int, dry_run: bool) -> str:
    """
    Generate a confirmation message based on the number of repositories and mode.
    """
    mode = "dry-run (no changes)" if dry_run else "actual clone/pull"
    return f"\nYou are about to process {repo_count} repository(ies) with {mode}."
