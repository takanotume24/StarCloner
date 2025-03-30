import requests
import sys
from typing import Dict, List, Optional
from types.repo_info import RepoInfo


def fetch_starred_repositories(username: str, token: Optional[str]) -> List[RepoInfo]:
    """
    Fetch all repositories starred by the given user (via GitHub API).
    """
    all_repos: List[RepoInfo] = []
    page: int = 1
    headers: Dict[str, str] = {"Accept": "application/vnd.github.v3+json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    while True:
        url = f"https://api.github.com/users/{username}/starred"
        params = {"page": page, "per_page": 100}
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
            break  # No more data

        for item in data:
            repo_info = RepoInfo(
                full_name=item["full_name"],
                clone_url=item["clone_url"],
                stargazers_count=item["stargazers_count"],
                owner_name=item["owner"]["login"],
            )
            all_repos.append(repo_info)

        page += 1

    return all_repos
