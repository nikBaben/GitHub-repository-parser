from datetime import (
    datetime, 
    timedelta, 
    timezone
)


class CachePolicy:
    """
    Политика кэширования на основе TTL (time-to-live).

    Определяет, является ли кэш актуальным, и вычисляет момент,
    с которого нужно обновлять данные с учётом overlap.

    Все операции приводят datetime к UTC.
    """
    def __init__(self, ttl: timedelta) -> None:
        self._ttl = ttl

    def is_fresh(
        self,
        cached_at: datetime,
        now: datetime | None = None,
    ) -> bool:
        """Проверяет, актуальны ли закэшированные данные."""
        now = now or datetime.now(timezone.utc)
        cached_at = self._to_aware_utc(cached_at)

        return now - cached_at <= self._ttl

    def refresh_from(
        self,
        cached_at: datetime,
        overlap: timedelta = timedelta(minutes=5),
    ) -> datetime:
        """
        Вычисляет момент, с которого нужно обновлять данные.

        Использует overlap, чтобы захватить часть уже полученных данных
        и избежать потери событий на границе обновления.
        """
        return self._to_aware_utc(cached_at) - overlap

    def _to_aware_utc(self, value: datetime) -> datetime:
        """
        Приводит datetime к timezone-aware UTC.

        Если datetime наивный (без tzinfo), считается, что он уже в UTC.
        """
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
