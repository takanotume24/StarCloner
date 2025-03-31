import subprocess
from pathlib import Path
from pytypes.repo_info import RepoInfo


def clone_or_pull_repo(repo: RepoInfo, target_dir: Path, dry_run: bool) -> None:
    """
    Clone or pull a repository into target_dir.
      - If the directory doesn't exist, perform a clone.
      - If it exists, perform a 'git pull'.
    """
    local_repo_dir_name = repo.full_name.split("/")[-1]
    user_or_org_name = repo.full_name.split("/")[0]
    local_path = target_dir / user_or_org_name / local_repo_dir_name

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
                f"Cloning {repo.clone_url} into '{target_dir}' (Repository: {repo.full_name})"
            )
            local_path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "clone", repo.clone_url], cwd=str(local_path.parent), check=False
            )
