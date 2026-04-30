from .base import GitHubPaginatedQuery


class ContributorsQuery(GitHubPaginatedQuery):
    anon: bool = True
