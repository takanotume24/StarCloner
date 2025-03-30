from typing import List, Optional
from types.repo_info import RepoInfo


def filter_star_repositories(
    repos: List[RepoInfo],
    min_stars: Optional[int],
    max_stars: Optional[int],
    owner_filter: Optional[str],
) -> List[RepoInfo]:
    """
    Filter starred repositories based on stargazer count and/or owner name.
    """

    def _star_filter(r: RepoInfo) -> bool:
        if min_stars is not None and r.stargazers_count < min_stars:
            return False
        if max_stars is not None and r.stargazers_count > max_stars:
            return False
        if owner_filter is not None and r.owner_name.lower() != owner_filter.lower():
            return False
        return True

    return list(filter(_star_filter, repos))
