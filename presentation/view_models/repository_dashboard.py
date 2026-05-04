from pydantic import BaseModel, ConfigDict

from presentation.chart.line_chart import HistoryChartModel
from .repository_analytics import RepositoryAnalyticsViewModel
from .repository_summary import RepositorySummaryViewModel


class RepositoryDashboardMetricViewModel(BaseModel):
    """Модель метрики для дашборда репозитория."""
    name: str
    title: str
    chart: HistoryChartModel

    model_config = ConfigDict(frozen=True)


class RepositoryDashboardViewModel(BaseModel):
    """Модель данных дашборда репозитория."""
    metrics: list[RepositoryDashboardMetricViewModel]
    summary: RepositorySummaryViewModel
    analytics: RepositoryAnalyticsViewModel

    model_config = ConfigDict(frozen=True)
