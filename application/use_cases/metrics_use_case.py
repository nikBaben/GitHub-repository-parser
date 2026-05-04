from application.dto import RepositoryAnalyticsDTO, RepositoryHistoryDTO
from domain.services import CountMetricsService, RepositoryScoringService


class СountMetricsRepositoryUseCase:
    def __init__(
        self,
        count_metrics_service: CountMetricsService,
        scoring_service: RepositoryScoringService,
    ) -> None:
        """Use Case для расчёта метрик и скоринга репозитория."""
        self._count_metrics_service = count_metrics_service
        self._scoring_service = scoring_service

    def execute(self, history: RepositoryHistoryDTO) -> RepositoryAnalyticsDTO:
        metrics = self._count_metrics_service.build_count_metrics(
            repository=history.repository,
            forks=history.forks,
            pulls=history.pulls,
            commits=history.commits,
            stars=history.stars,
            merged_pulls=history.merged_pulls,
            issues=history.issues,
            contributors=history.contributors,
        )

        score = self._scoring_service.calculate(metrics)

        return RepositoryAnalyticsDTO(
            repository=history.repository,
            archived=score.archived,
            stars=score.stars,
            forks=score.forks,
            pulls=score.pulls,
            commits=score.commits,
            merged_pulls=score.merged_pulls,
            issues=score.issues,
            contributors=score.contributors,
            watchers=score.watchers,
            open_issues=score.open_issues,
            last_push=score.last_push,
            popularity_score=score.popularity_score,
            activity_score=score.activity_score,
            engagement_score=score.engagement_score,
            demand_score=score.demand_score,
        )