import unittest
from unittest.mock import patch, Mock
from functions.fetch_user_repositories import fetch_user_repositories
from pytypes.repo_info import RepoInfo


class TestFetchUserRepositories(unittest.TestCase):
    @patch(
        "functions.fetch_user_repositories.requests.get",
    )
    def test_fetch_user_repositories(self, mock_get):
        mock_response_page_1 = Mock()
        mock_response_page_1.status_code = 200
        mock_response_page_1.json.return_value = [
            {
                "full_name": "octocat/repo1",
                "clone_url": "https://github.com/octocat/repo1.git",
                "stargazers_count": 50,
                "owner": {"login": "octocat"},
                "fork": False,
                "archived": False,
            }
        ]

        mock_response_page_2 = Mock()
        mock_response_page_2.status_code = 200
        mock_response_page_2.json.return_value = []

        mock_get.side_effect = [mock_response_page_1, mock_response_page_2]
        result = fetch_user_repositories(
            "octocat", None, include_forks=False, include_archived=False
        )
        expected = [
            RepoInfo(
                full_name="octocat/repo1",
                clone_url="https://github.com/octocat/repo1.git",
                stargazers_count=50,
                owner_name="octocat",
            )
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
