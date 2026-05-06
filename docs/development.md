# Разработка

## Установка dev-зависимостей

```bash
python -m pip install ".[dev]"
```

## Проверка Ruff

```bash
ruff check .
```

## Тесты

Если тесты добавлены:
Пока что нет.
```bash
pytest
```

## Как добавить новую метрику

Обычно нужно пройти весь путь данных:

```text
GitHub API
  -> parser.infrastructure adapter
  -> parser.domain history/value object
  -> parser.application DTO
  -> CountMetricsService
  -> RepositoryScoringService, если метрика влияет на score
  -> parser.presentation mapper
  -> dashboard view model
  -> Plotly dashboard
```

## Как добавить новый график

1. Добавить или использовать существующую историю в `RepositoryHistoryDTO`.
2. Добавить метод в `HistoryChartMapper`.
3. Добавить `RepositoryDashboardMetricViewModel` в `RepositoryDashboardMapper`.
4. Проверить, что Plotly dashboard корректно переключает новую метрику.

