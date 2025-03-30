import unittest
from io import StringIO
from unittest.mock import patch
from functions.print_repositories import print_repositories
from types.repo_info import RepoInfo


class TestPrintRepositories(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_print_repositories(self, mock_stdout):
        repos = [
            RepoInfo(
                full_name="repo1",
                clone_url="",
                stargazers_count=50,
                owner_name="owner1",
            ),
            RepoInfo(
                full_name="repo2",
                clone_url="",
                stargazers_count=150,
                owner_name="owner2",
            ),
        ]
        print_repositories(repos)
        expected_output = (
            "Repositories to process (total 2), sorted alphabetically:\n"
            "  repo1 (Stars: 50, Owner: owner1)\n"
            "  repo2 (Stars: 150, Owner: owner2)\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()
