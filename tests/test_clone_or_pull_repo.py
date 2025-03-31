import unittest
from unittest.mock import patch, Mock
from pathlib import Path
from functions.clone_or_pull_repo import clone_or_pull_repo
from pytypes.repo_info import RepoInfo


class TestCloneOrPullRepo(unittest.TestCase):
    @patch("functions.clone_or_pull_repo.subprocess.run")
    @patch("functions.clone_or_pull_repo.Path.is_dir")
    def test_clone_or_pull_repo_clone(self, mock_is_dir, mock_run):
        mock_is_dir.return_value = False
        repo = RepoInfo(
            full_name="octocat/repo1",
            clone_url="https://github.com/octocat/repo1.git",
            stargazers_count=50,
            owner_name="octocat",
        )
        target_dir = Path("/fake/dir")
        user_or_org_name = repo.full_name.split("/")[0]
        clone_or_pull_repo(repo, target_dir, dry_run=False)
        expected_path = target_dir / user_or_org_name / "repo1"
        mock_run.assert_called_with(
            ["git", "clone", repo.clone_url], cwd=str(expected_path.parent), check=False
        )

    @patch("functions.clone_or_pull_repo.subprocess.run")
    @patch("functions.clone_or_pull_repo.Path.is_dir")
    def test_clone_or_pull_repo_pull(self, mock_is_dir, mock_run):
        mock_is_dir.return_value = True
        repo = RepoInfo(
            full_name="octocat/repo1",
            clone_url="https://github.com/octocat/repo1.git",
            stargazers_count=50,
            owner_name="octocat",
        )
        target_dir = Path("/fake/dir")
        user_or_org_name = repo.full_name.split("/")[0]
        clone_or_pull_repo(repo, target_dir, dry_run=False)
        expected_path = target_dir / user_or_org_name / "repo1"
        mock_run.assert_called_with(
            ["git", "-C", str(expected_path), "pull"], check=False
        )


if __name__ == "__main__":
    unittest.main()
