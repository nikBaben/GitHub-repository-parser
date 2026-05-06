from pathlib import Path
from datetime import datetime, timezone

from pydantic import ValidationError

from parser.application.dto import CachedHistoryDTO, RepositoryHistoryDTO
from parser.application.queries.queries import GetHistoryQuery


class JsonHistoryStorageAdapter:
    """Адаптер для хранения кэшированных исторических данных в JSON-файлах."""
    def __init__(self, base_path: str = "data/json") -> None:
        self._base_path = Path(base_path)

    def _build_path(self, query: GetHistoryQuery) -> Path:
        """
        Строит путь к файлу кэша по текущей схеме именования.
        Формат:
            {base_path}/{owner}/{repo}/{period}.json
        Где:
            - period = "all" если days=None
            - period = "days_N" если задан диапазон
        """
        period = "all" if query.days is None else f"days_{query.days}"

        return self._base_path / query.owner / query.repo / f"{period}.json"

    def save(self, query: GetHistoryQuery, cached: CachedHistoryDTO) -> None:
        """ 
        Сохраняет кэшированные данные в JSON-файл.
        Автоматически создаёт необходимые директории.
        """
        path = self._build_path(query)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(cached.model_dump_json(indent=2))

    def load(self, query: GetHistoryQuery) -> CachedHistoryDTO | None:
        """Загружает кэшированные данные из JSON-файла."""
        path = self._build_path(query)

        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            raw_json = f.read()

        try:
            return CachedHistoryDTO.model_validate_json(raw_json)
        except ValidationError:
            history = RepositoryHistoryDTO.model_validate_json(raw_json)
            cached_at = path.stat().st_mtime

            return CachedHistoryDTO(
                cached_at=datetime.fromtimestamp(cached_at, tz=timezone.utc),
                history=history,
            )
