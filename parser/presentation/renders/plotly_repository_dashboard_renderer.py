from parser.presentation.view_models import RepositoryDashboardViewModel
from parser.presentation.plotters.plotly_analytics_dashboard_plotter import (
    PlotlyAnalyticsDashboardPlotter,
)


class PlotlyRepositoryDashboardRenderer:
    """Рендерер дашборда репозитория с использованием Plotly."""
    def show(self, dashboard: RepositoryDashboardViewModel) -> None:
        """Отображает интерактивный дашборд репозитория."""
        PlotlyAnalyticsDashboardPlotter.show(dashboard)

    def save_html(
        self,
        dashboard: RepositoryDashboardViewModel,
        filepath: str,
    ) -> None:
        """Сохраняет интерактивный дашборд репозитория в HTML-файл."""
        PlotlyAnalyticsDashboardPlotter.save_html(
            dashboard=dashboard,
            filepath=filepath,
        )
