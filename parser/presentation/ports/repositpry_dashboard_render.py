from typing import Protocol

from parser.presentation.view_models import RepositoryDashboardViewModel


class RepositoryDashboardRendererPort(Protocol):
    """Порт рендерера дашборда репозитория."""
    def show(self, dashboard: RepositoryDashboardViewModel) -> None:
        """Отображает дашборд репозитория."""
        ...

    def save_html(
        self,
        dashboard: RepositoryDashboardViewModel,
        filepath: str,
    ) -> None:
        """Сохраняет дашборд репозитория в HTML-файл."""
        ...
