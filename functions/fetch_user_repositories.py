import requests
import sys
from typing import Dict, List, Optional
from pytypes.repo_info import RepoInfo


def fetch_user_repositories(
    username: str, token: Optional[str], include_forks: bool, include_archived: bool
) -> List[RepoInfo]:
    """
    Fetch all repositories owned by the given user (via GitHub API).
    Optionally include forked or archived repositories based on arguments.
    """
    all_repos: List[RepoInfo] = []
    page: int = 1
    headers: Dict[str, str] = {"Accept": "application/vnd.github.v3+json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    while True:
        url = f"https://api.github.com/users/{username}/repos"
        params = {
            "page": page,
            "per_page": 100,
            "type": "all",  # 'all' includes private, forks, etc., if authorized
            "sort": "full_name",
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(
                f"Error: GitHub API request returned {response.status_code}.",
                file=sys.stderr,
            )
            print("Response body:", response.text, file=sys.stderr)
            break

        data = response.json()
        if not data:
            break

        for item in data:
            if not include_forks and item["fork"]:
                continue
            if not include_archived and item["archived"]:
                continue

            repo_info = RepoInfo(
                full_name=item["full_name"],
                clone_url=item["clone_url"],
                stargazers_count=item["stargazers_count"],
                owner_name=item["owner"]["login"],
            )
            all_repos.append(repo_info)

        page += 1

    return all_repos
