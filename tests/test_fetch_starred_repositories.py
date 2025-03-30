import unittest
from unittest.mock import patch, Mock
from functions.fetch_starred_repositories import fetch_starred_repositories
from types.repo_info import RepoInfo


class TestFetchStarredRepositories(unittest.TestCase):
    @patch("functions.fetch_starred_repositories.requests.get")
    def test_fetch_starred_repositories(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "full_name": "octocat/repo1",
                "clone_url": "https://github.com/octocat/repo1.git",
                "stargazers_count": 50,
                "owner": {"login": "octocat"},
            }
        ]
        mock_get.return_value = mock_response

        result = fetch_starred_repositories("octocat", None)
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
