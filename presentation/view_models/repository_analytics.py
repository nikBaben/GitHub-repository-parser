from pydantic import BaseModel, ConfigDict


class RepositoryAnalyticsViewModel(BaseModel):
    """Аналитические показатели репозитория."""
    stars_metric: int
    active_forks: int
    pulls_metric: int
    commits_metric: int
    merged_pulls: int
    issues_metric: int
    contributors: int
    popularity: float
    activity: float
    engagement: float
    demand: float

    model_config = ConfigDict(frozen=True)
