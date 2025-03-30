import unittest
from argparse import Namespace
from functions.filter_repositories import filter_repositories
from types.repo_info import RepoInfo


class TestFilterRepositories(unittest.TestCase):
    def test_filter_repositories_star(self):
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
        args = Namespace(
            command="star", min_stars=100, max_stars=200, owner_filter=None
        )
        result = filter_repositories(args, repos)
        expected = [
            RepoInfo(
                full_name="repo2",
                clone_url="",
                stargazers_count=150,
                owner_name="owner2",
            ),
        ]
        self.assertEqual(result, expected)

    def test_filter_repositories_repo(self):
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
        args = Namespace(command="repo")
        result = filter_repositories(args, repos)
        expected = repos
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
