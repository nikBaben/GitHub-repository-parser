from parser.application.dto import RepositoryAnalyticsDTO
from parser.presentation.view_models.repository_summary import RepositorySummaryViewModel


class RepositorySummaryMapper:
    """Маппер сводной информации о репозитории в модель представления."""
    @staticmethod
    def to_view_model(analytics: RepositoryAnalyticsDTO) -> RepositorySummaryViewModel:
        """Преобразует аналитические данные репозитория в сводную модель представления."""
        repository = analytics.repository
        return RepositorySummaryViewModel(
            full_name=f"{repository.owner_login}/{repository.name}",
            stars=analytics.stars.stars,
            watchers=repository.watchers,
            open_issues=repository.open_issues,
            archived=repository.archived,
            total_forks=analytics.forks.forks,
            total_pulls=analytics.pulls.pulls,
            total_commits=analytics.commits.commits,
        )
