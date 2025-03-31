import tempfile
from pathlib import Path
from functions.list_cloned_repositories import list_cloned_repositories
from pytypes.repo_info import RepoInfo
from unittest.mock import patch


def test_list_cloned_repositories(capsys):
    # Create a temporary directory to simulate cloned repositories
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        # Simulate user directories and cloned repositories
        user_dir = temp_path / "user1"
        user_dir.mkdir()
        repo_dir = user_dir / "repo1"
        repo_dir.mkdir()

        # Expected output
        expected_repo_info = RepoInfo(
            full_name="user1/repo1",
            clone_url="",
            stargazers_count=0,
            owner_name="user1",
        )

        # Run the function
        with patch(
            "functions.list_cloned_repositories.print_repositories"
        ) as mock_print:
            list_cloned_repositories(temp_path)
            mock_print.assert_called_once_with([expected_repo_info])
