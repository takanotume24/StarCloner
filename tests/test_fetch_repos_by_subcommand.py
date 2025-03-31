import unittest
from unittest.mock import patch, MagicMock
from functions.fetch_repos_by_subcommand import fetch_repos_by_subcommand
from argparse import Namespace
from pytypes.repo_info import RepoInfo

class TestFetchReposBySubcommand(unittest.TestCase):
    @patch('functions.fetch_repos_by_subcommand.fetch_user_repositories')
    def test_fetch_user_repositories_success(self, mock_fetch_user_repositories):
        # Mock the return value of fetch_user_repositories
        mock_fetch_user_repositories.return_value = [
            RepoInfo(
                full_name="user/repo1",
                clone_url="https://github.com/user/repo1.git",
                stargazers_count=10,
                owner_name="user"
            )
        ]

        args = Namespace(command="repo", username="user", include_forks=False, include_archived=False)
        token = "fake-token"

        repos = fetch_repos_by_subcommand(args, token)

        # Assert that the function returns a non-empty list
        self.assertTrue(repos)
        self.assertEqual(len(repos), 1)
        self.assertEqual(repos[0].full_name, "user/repo1")

    @patch('functions.fetch_user_repositories.fetch_user_repositories')
    def test_fetch_user_repositories_failure(self, mock_fetch_user_repositories):
        # Mock the return value of fetch_user_repositories to simulate an error
        mock_fetch_user_repositories.return_value = []

        args = Namespace(command="repo", username="user", include_forks=False, include_archived=False)
        token = "fake-token"

        repos = fetch_repos_by_subcommand(args, token)

        # Assert that the function returns an empty list
        self.assertFalse(repos)

if __name__ == '__main__':
    unittest.main()
