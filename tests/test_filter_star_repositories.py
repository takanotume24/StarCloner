import unittest
from functions.filter_star_repositories import filter_star_repositories
from types.repo_info import RepoInfo


class TestFilterStarRepositories(unittest.TestCase):
    def test_filter_star_repositories(self):
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
            RepoInfo(
                full_name="repo3",
                clone_url="",
                stargazers_count=200,
                owner_name="owner1",
            ),
        ]

        result = filter_star_repositories(
            repos, min_stars=100, max_stars=200, owner_filter="owner1"
        )
        expected = [
            RepoInfo(
                full_name="repo3",
                clone_url="",
                stargazers_count=200,
                owner_name="owner1",
            ),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
