import unittest
from pathlib import Path
from functions.get_github_user_repo_from_config import get_github_user_repo_from_config

class TestGetGithubUserRepoFromConfig(unittest.TestCase):
    def test_valid_config(self):
        # Create a temporary .git/config file with valid content
        config_content = "[remote \"origin\"]\n\turl = https://github.com/user/repo.git\n"
        config_path = Path("temp_config")
        config_path.write_text(config_content, encoding="utf-8")

        user, repo = get_github_user_repo_from_config(config_path)
        self.assertEqual(user, "user")
        self.assertEqual(repo, "repo")

        config_path.unlink()  # Clean up

    def test_invalid_config(self):
        # Create a temporary .git/config file with invalid content
        config_content = "[remote \"origin\"]\n\turl = https://example.com/user/repo.git\n"
        config_path = Path("temp_config")
        config_path.write_text(config_content, encoding="utf-8")

        user, repo = get_github_user_repo_from_config(config_path)
        self.assertIsNone(user)
        self.assertIsNone(repo)

        config_path.unlink()  # Clean up

    def test_no_config_file(self):
        # Test with a non-existent config file
        config_path = Path("non_existent_config")
        user, repo = get_github_user_repo_from_config(config_path)
        self.assertIsNone(user)
        self.assertIsNone(repo)

if __name__ == "__main__":
    unittest.main()
