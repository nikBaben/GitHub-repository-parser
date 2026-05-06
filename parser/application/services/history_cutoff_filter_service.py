from typing import Any

from datetime import datetime, timezone

from parser.application.dto import RepositoryHistoryDTO


class HistoryCutoffFilter:
    """
    Фильтр исторических данных по дате отсечения (cutoff).

    Применяет фильтрацию ко всем типам историй внутри RepositoryHistoryDTO,
    оставляя только точки, дата которых больше или равна cutoff_dt
    """
    def apply(
        self,
        history: RepositoryHistoryDTO,
        cutoff_dt: datetime | None,
    ) -> RepositoryHistoryDTO:
        """Применяет фильтр cutoff ко всем историям внутри DTO."""
        if cutoff_dt is None:
            return history

        cutoff_dt = self._to_aware_utc(cutoff_dt)

        return history.model_copy(
            update={
                "stars": self._filter_points(
                    history.stars,
                    cutoff_dt,
                    "starred_at",
                ),
                "forks": self._filter_points(
                    history.forks,
                    cutoff_dt,
                    "forked_at",
                ),
                "pulls": self._filter_points(
                    history.pulls,
                    cutoff_dt,
                    "pulled_at",
                ),
                "commits": self._filter_points(
                    history.commits,
                    cutoff_dt,
                    "committed_at",
                ),
                "merged_pulls": self._filter_points(
                    history.merged_pulls,
                    cutoff_dt,
                    "merged_at",
                ),
                "issues": self._filter_points(
                    history.issues,
                    cutoff_dt,
                    "issued_at",
                ),
                "contributors": self._filter_points(
                    history.contributors,
                    cutoff_dt,
                    "contirbuted_at",
                ),
            },
        )

    def _filter_points(
        self,
        history: Any,
        cutoff_dt: datetime,
        date_field: str,
    ) -> Any:
        """Фильтрует точки конкретной истории по дате."""
        return history.model_copy(
            update={
                "points": [
                    point
                    for point in history.points
                    if self._to_aware_utc(getattr(point, date_field)) >= cutoff_dt
                ],
            },
        )

    def _to_aware_utc(self, value: datetime) -> datetime:
        """Приводит datetime к timezone-aware UTC."""
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
