from parser.application.dto import RepositoryAnalyticsDTO
from parser.presentation.view_models.repository_analytics import RepositoryAnalyticsViewModel


class RepositoryAnalyticsMapper:
    """Маппер аналитических данных репозитория в модель представления."""
    @staticmethod
    def to_view_model(analytics: RepositoryAnalyticsDTO) -> RepositoryAnalyticsViewModel:
        """Преобразует аналитические данные репозитория в модель представления."""
        return RepositoryAnalyticsViewModel(
            stars_metric=analytics.stars.stars,
            active_forks=analytics.forks.forks,
            pulls_metric=analytics.pulls.pulls,
            commits_metric=analytics.commits.commits,
            merged_pulls=analytics.merged_pulls.merged_pulls,
            issues_metric=analytics.issues.issues,
            contributors=analytics.contributors.contributors,
            popularity=analytics.popularity_score.popularity_score,
            activity=analytics.activity_score.activity_score,
            engagement=analytics.engagement_score.engagement_score,
            demand=analytics.demand_score.demand_score,
        )
