from infrastructure.github.config import settings


def repository_url(owner: str, repo: str) -> str:
    """Базовый URL для GitHub-репозитория."""
    return f"{settings.GITHUB_API_URL}/repos/{owner}/{repo}"


def stargazers_url(owner: str, repo: str) -> str:
    """URL для получения списка звезд."""
    return f"{repository_url(owner, repo)}/stargazers"


def forks_url(owner: str, repo: str) -> str:
    """URL для получения списка форков репозитория."""
    return f"{repository_url(owner, repo)}/forks"


def pulls_url(owner: str, repo: str) -> str:
    """URL для получения списка пуллов репозитория."""
    return f"{repository_url(owner, repo)}/pulls"


def commits_url(owner: str, repo: str) -> str:
    """URL для получения списка коммитов репозитория."""
    return f"{repository_url(owner, repo)}/commits"


def contributors_url(owner: str, repo: str) -> str:
    """URL для получения списка контрибьюторов репозитория."""
    return f"{repository_url(owner, repo)}/contributors"


def issues_url(owner: str, repo: str) -> str:
    """URL для получения списка ишьюсов репозитория."""
    return f"{repository_url(owner, repo)}/issues"