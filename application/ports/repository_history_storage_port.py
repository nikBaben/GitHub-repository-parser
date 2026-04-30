from typing import Protocol

from application.dto import CachedHistoryDTO
from application.queries.queries import GetHistoryQuery


class RepositoryHistoryStoragePort(Protocol):
    """Порт для работы с хранилищем кэша исторических данных репозитория."""

    def save(self, query: GetHistoryQuery, cached: CachedHistoryDTO) -> None:
        """Сохраняет кэшированные данные для заданного запроса."""
        ...

    def load(self, query: GetHistoryQuery) -> CachedHistoryDTO | None:
        """Загружает кэшированные данные для заданного запроса."""
        ...
