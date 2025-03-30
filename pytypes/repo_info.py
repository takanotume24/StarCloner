from dataclasses import dataclass


@dataclass
class RepoInfo:
    """
    Holds information about a GitHub repository.
    """

    full_name: str
    clone_url: str
    stargazers_count: int
    owner_name: str
