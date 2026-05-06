# Структура проекта

```text
Repository-Parser/
  parser/
    application/
      dto/
      ports/
      queries/
      services/
      use_cases/

    domain/
      entities/
      services/
      value_objects/
      utils.py

    infrastructure/
      adapters/
      datasets/
      di/
      github/

    presentation/
      chart/
      mappers/
      plotters/
      ports/
      renders/
      view_models/

  data/
    csv/kaggle/
    json/

  main.py
  pyproject.toml
  Dockerfile
  docker-compose.yml
  .env.example
```

## `parser/application`

Слой сценариев приложения.

- `dto/` - объекты передачи данных между слоями.
- `ports/` - интерфейсы, от которых зависит application layer.
- `queries/` - входные query-модели, например `GetHistoryQuery`.
- `services/` - сервисы загрузки, кэширования, merge и фильтрации истории.
- `use_cases/` - use cases для получения истории и расчета аналитики.

## `parser/domain`

Слой бизнес-логики.

- `entities/` - основные модели репозитория, истории, метрик и score.
- `value_objects/` - типизированные значения: stars, forks, issues и другие.
- `services/` - расчет метрик и скоринга.
- `utils.py` - функции нормализации score.

## `parser/infrastructure`

Слой внешних зависимостей.

- `adapters/` - адаптер GitHub history и JSON storage.
- `datasets/` - провайдер score-конфига на базе Kaggle CSV.
- `di/` - composition root.
- `github/` - HTTP-клиент, endpoints, queries, mappers.

## `parser/presentation`

Слой подготовки результата.

- `chart/` - модели графиков.
- `mappers/` - преобразование history/analytics в view models.
- `plotters/` - построители Plotly-графиков.
- `ports/` - интерфейс renderer.
- `renders/` - реализация renderer.
- `view_models/` - модели представления dashboard.

## `data`

- `data/csv/kaggle/github_repos.csv` - датасет для настройки скоринга.
- `data/json/` - runtime-кэш истории. Создается автоматически.
