from datetime import datetime, timezone

from application.dto import RepositoryHistoryDTO
from application.queries.queries import GetHistoryQuery
from application.services.history_cache_service import HistoryCacheService
from application.services.history_cutoff_filter_service import HistoryCutoffFilter
from application.services.history_loader import HistoryLoader
from application.services.history_merger import HistoryMerger


class HistoryService:
    """Cервис для получения исторических данных репозитория."""
    def __init__(
        self,
        loader: HistoryLoader,
        cache: HistoryCacheService,
        merger: HistoryMerger,
        cutoff_filter: HistoryCutoffFilter,
    ) -> None:
        self._loader = loader
        self._cache = cache
        self._merger = merger
        self._cutoff_filter = cutoff_filter

    async def get_history(self, query: GetHistoryQuery) -> RepositoryHistoryDTO:
        """Получает исторические данные репозитория с учётом кэширования."""
        now = datetime.now(timezone.utc)
        cutoff_dt = query.cutoff_dt
        cached = self._cache.load(query)

        if cached is not None and self._cache.is_fresh(cached.cached_at, now):
            return self._cutoff_filter.apply(cached.history, cutoff_dt)

        if cached is not None:
            refresh_from = self._cache.refresh_from(cached.cached_at)
            patch = await self._loader.load(query, refresh_from)
            history = self._merger.merge(cached.history, patch)
            history = self._cutoff_filter.apply(history, cutoff_dt)
            self._cache.save(query, history)

            return history

        history = await self._loader.load(query, cutoff_dt)
        history = self._cutoff_filter.apply(history, cutoff_dt)
        self._cache.save(query, history)

        return history
