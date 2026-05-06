from datetime import datetime

from pydantic import BaseModel

from parser.application.dto import RepositoryHistoryDTO


class CachedHistoryDTO(BaseModel):
    """
    DTO для хранения исторических данных репозитория в кэше.

    Оборачивает RepositoryHistoryDTO, добавляя метаинформацию
    о времени кэшировани.
    """
    cached_at: datetime
    history: RepositoryHistoryDTO
