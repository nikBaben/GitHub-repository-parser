from datetime import datetime, timezone
from typing import Any

from parser.application.dto import RepositoryHistoryDTO


class HistoryMerger:
    """Сервис для объединения двух наборов исторических данных."""
    def merge(
        self,
        current: RepositoryHistoryDTO,
        patch: RepositoryHistoryDTO,
    ) -> RepositoryHistoryDTO:
        """Объединяет текущую историю с новой."""
        return current.model_copy(
            update={
                "repository": patch.repository,
                "stars": self._merge_points(
                    current.stars,
                    patch.stars,
                    "starred_at",
                ),
                "forks": self._merge_points(
                    current.forks,
                    patch.forks,
                    "forked_at",
                ),
                "pulls": self._merge_points(
                    current.pulls,
                    patch.pulls,
                    "pulled_at",
                ),
                "commits": self._merge_points(
                    current.commits,
                    patch.commits,
                    "committed_at",
                ),
                "merged_pulls": self._merge_points(
                    current.merged_pulls,
                    patch.merged_pulls,
                    "merged_at",
                ),
                "issues": self._merge_points(
                    current.issues,
                    patch.issues,
                    "issued_at",
                ),
                "contributors": self._merge_points(
                    current.contributors,
                    patch.contributors,
                    "contirbuted_at",
                ),
            },
        )

    def _merge_points(
        self,
        current: Any,
        patch: Any,
        date_field: str,
    ) -> Any:
        """Объединяет точки конкретной истории."""
        points_by_key = {
            point.model_dump_json(): point
            for point in current.points
        }
        points_by_key.update(
            {
                point.model_dump_json(): point
                for point in patch.points
            }
        )
        points = sorted(
            points_by_key.values(),
            key=lambda point: self._to_aware_utc(getattr(point, date_field)),
        )

        return current.model_copy(
            update={
                "points": points,
                "generated_at": patch.generated_at,
            },
        )

    def _to_aware_utc(self, value: datetime) -> datetime:
        """Приводит datetime к timezone-aware UTC."""
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
