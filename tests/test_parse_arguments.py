import unittest
import sys
from argparse import Namespace
from functions.parse_arguments import parse_arguments


class TestParseArguments(unittest.TestCase):
    def test_parse_arguments_star(self):
        test_args = [
            "starcloner",
            "star",
            "octocat",
            "--dry-run",
            "--yes",
            "--min-stars=10",
            "--max-stars=100",
            "--owner-filter=owner",
            "--output-dir=./output",
        ]
        sys.argv = test_args
        args = parse_arguments()
        expected = Namespace(
            command="star",
            username="octocat",
            dry_run=True,
            yes=True,
            min_stars=10,
            max_stars=100,
            owner_filter="owner",
            output_dir="./output",
        )
        self.assertEqual(args, expected)

    def test_parse_arguments_repo(self):
        test_args = [
            "starcloner",
            "repo",
            "octocat",
            "--dry-run",
            "--yes",
            "--include-forks",
            "--include-archived",
            "--output-dir=./output",
        ]
        sys.argv = test_args
        args = parse_arguments()
        expected = Namespace(
            command="repo",
            username="octocat",
            dry_run=True,
            yes=True,
            include_forks=True,
            include_archived=True,
            output_dir="./output",
        )
        self.assertEqual(args, expected)

    def test_parse_arguments_org(self):
        test_args = [
            "starcloner",
            "org",
            "github",
            "--dry-run",
            "--yes",
            "--include-forks",
            "--include-archived",
            "--output-dir=./output",
        ]
        sys.argv = test_args
        args = parse_arguments()
        expected = Namespace(
            command="org",
            orgname="github",
            dry_run=True,
            yes=True,
            include_forks=True,
            include_archived=True,
            output_dir="./output",
        )
        self.assertEqual(args, expected)


if __name__ == "__main__":
    unittest.main()
