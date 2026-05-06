from parser.application.dto import RepositoryAnalyticsDTO, RepositoryHistoryDTO
from parser.presentation.view_models.repository_dashboard import (
    RepositoryDashboardMetricViewModel,
    RepositoryDashboardViewModel,
)
from parser.presentation.mappers.repository_analytics_chart_mapper import (
    BucketType,
    HistoryChartMapper,
)
from parser.presentation.mappers.repository_analytics_mapper import RepositoryAnalyticsMapper
from parser.presentation.mappers.repository_summary_mapper import RepositorySummaryMapper


class RepositoryDashboardMapper:
    """Маппер истории и аналитики репозитория в модель представления дашборда."""
    @classmethod
    def to_view_model(
        cls,
        history: RepositoryHistoryDTO,
        analytics: RepositoryAnalyticsDTO,
        bucket: BucketType = "week",
    ) -> RepositoryDashboardViewModel:
        """Преобразует историю и аналитику репозитория в модель представления дашборда."""
        return RepositoryDashboardViewModel(
            metrics=[
                RepositoryDashboardMetricViewModel(
                    name="Forks",
                    title="Forks history",
                    chart=HistoryChartMapper.to_forks_chart(history, bucket=bucket),
                ),
                RepositoryDashboardMetricViewModel(
                    name="Pull requests",
                    title="Pull requests history",
                    chart=HistoryChartMapper.to_pulls_chart(history, bucket=bucket),
                ),
                RepositoryDashboardMetricViewModel(
                    name="Commits",
                    title="Commits history",
                    chart=HistoryChartMapper.to_commits_chart(history, bucket=bucket),
                ),
                RepositoryDashboardMetricViewModel(
                    name="Stars",
                    title="Stars history",
                    chart=HistoryChartMapper.to_stars_chart(history, bucket=bucket),
                ),
                RepositoryDashboardMetricViewModel(
                    name="Merged pulls",
                    title="Merged pulls history",
                    chart=HistoryChartMapper.to_merged_pulls_chart(
                        history,
                        bucket=bucket,
                    ),
                ),
                RepositoryDashboardMetricViewModel(
                    name="Issues",
                    title="Issues history",
                    chart=HistoryChartMapper.to_issues_chart(history, bucket=bucket),
                ),
                RepositoryDashboardMetricViewModel(
                    name="Contributors",
                    title="Contributors history",
                    chart=HistoryChartMapper.to_contributors_charts(
                        history,
                        bucket=bucket,
                    ),
                ),
            ],
            summary=RepositorySummaryMapper.to_view_model(analytics),
            analytics=RepositoryAnalyticsMapper.to_view_model(analytics),
        )
