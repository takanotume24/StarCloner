from unittest.mock import patch, MagicMock
from functions.move_temp_files import move_temp_files


class TestMoveTempFiles:
    @patch("argparse.ArgumentParser.parse_args")
    @patch("functions.move_temp_files.Path")
    @patch("functions.move_temp_files.safe_move")
    @patch("functions.move_temp_files.get_github_user_repo_from_config")
    def test_move_temp_files(
        self,
        mock_get_github_user_repo_from_config,
        mock_safe_move,
        mock_path,
        mock_parse_args,
        tmpdir,
    ):
        # Mock the arguments
        mock_parse_args.return_value = MagicMock(
            target_directory=str(tmpdir), dry_run=False
        )

        # Mock the Path object and its methods
        mock_base_dir = MagicMock()
        mock_path.return_value.resolve.return_value = mock_base_dir
        mock_base_dir.is_dir.return_value = True
        mock_repo = MagicMock(is_dir=MagicMock(return_value=True), name="repo1")
        mock_base_dir.iterdir.return_value = [mock_repo]
        mock_target_dir = mock_base_dir / "user" / "repo"
        mock_target_dir.exists.return_value = False

        # Mock the .git directory and config path
        mock_git_dir = mock_base_dir.iterdir.return_value[0] / ".git"
        mock_git_dir.is_dir.return_value = True
        mock_config_path = mock_git_dir / "config"

        # Mock the get_github_user_repo_from_config function
        mock_get_github_user_repo_from_config.return_value = ("user", "repo")

        # Call the function
        move_temp_files(dry_run=False)

        # Assertions
        mock_get_github_user_repo_from_config.assert_called_once_with(mock_config_path)
        mock_safe_move.assert_called_once()
