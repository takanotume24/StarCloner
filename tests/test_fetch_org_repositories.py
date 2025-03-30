import unittest
from unittest.mock import patch, Mock
from functions.fetch_org_repositories import fetch_org_repositories
from types.repo_info import RepoInfo


class TestFetchOrgRepositories(unittest.TestCase):
    @patch("functions.fetch_org_repositories.requests.get")
    def test_fetch_org_repositories(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "full_name": "github/repo1",
                "clone_url": "https://github.com/github/repo1.git",
                "stargazers_count": 50,
                "owner": {"login": "github"},
                "fork": False,
                "archived": False,
            }
        ]
        mock_get.return_value = mock_response

        result = fetch_org_repositories(
            "github", None, include_forks=False, include_archived=False
        )
        expected = [
            RepoInfo(
                full_name="github/repo1",
                clone_url="https://github.com/github/repo1.git",
                stargazers_count=50,
                owner_name="github",
            )
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
