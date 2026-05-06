from typing import Protocol

from parser.domain.services import ScoreConfig


class ScoreConfigPort(Protocol):
    """Порт для получения конфигурации скоринга репозитория."""
    def get_config(self) -> ScoreConfig:
        """Возвращает текущую конфигурацию скоринга."""
        ...