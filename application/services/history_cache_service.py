from datetime import datetime, timezone

from application.dto import CachedHistoryDTO, RepositoryHistoryDTO
from application.ports import RepositoryHistoryStoragePort
from application.queries.queries import GetHistoryQuery
from application.services.cache_policy import CachePolicy


class HistoryCacheService:
    """Cервис для работы с кэшем исторических данных репозитория."""
    def __init__(
        self,
        storage: RepositoryHistoryStoragePort,
        cache_policy: CachePolicy,
    ) -> None:
        self._storage = storage
        self._cache_policy = cache_policy

    def load(self, query: GetHistoryQuery) -> CachedHistoryDTO | None:
        """Загружает закэшированные данные по запросу."""
        return self._storage.load(query)

    def save(
        self,
        query: GetHistoryQuery,
        history: RepositoryHistoryDTO,
    ) -> None:
        """ 
        Сохраняет историю репозитория в кэш.
        Время сохранения фиксируется в UTC.
        """
        self._storage.save(
            query,
            CachedHistoryDTO(
                cached_at=datetime.now(timezone.utc),
                history=history,
            ),
        )

    def is_fresh(
        self,
        cached_at: datetime,
        now: datetime | None = None,
    ) -> bool:
        """ Проверяет, является ли кэш актуальным."""
        return self._cache_policy.is_fresh(cached_at, now)

    def refresh_from(self, cached_at: datetime) -> datetime:
        """Вычисляет момент, с которого нужно обновлять данные."""
        return self._cache_policy.refresh_from(cached_at)
