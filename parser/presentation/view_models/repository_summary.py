from pydantic import BaseModel, ConfigDict


class RepositorySummaryViewModel(BaseModel):
    """Сводная информация о репозитории."""
    full_name: str
    stars: int
    watchers: int
    open_issues: int
    archived: bool
    total_forks: int
    total_pulls: int
    total_commits: int

    model_config = ConfigDict(frozen=True)