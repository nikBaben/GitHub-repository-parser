# Скоринг

Проект рассчитывает четыре score-группы:

| Score | Смысл | Метрики |
| --- | --- | --- |
| `popularity` | Популярность репозитория | stars, forks |
| `activity` | Активность разработки | contributors, merged pull requests, commits |
| `engagement` | Вовлеченность | forks, issues |
| `demand` | Итоговый score | popularity, activity, engagement |

## Где находится логика

Основные файлы:

```text
domain/services/repository_metrics_service.py
domain/services/score_metrics_service.py
infrastructure/datasets/kaggle_provider.py
```

## CountMetricsService

`CountMetricsService` преобразует историю и состояние репозитория в агрегированные
метрики:

- archived;
- stars;
- pulls;
- commits;
- merged pulls;
- forks;
- issues;
- contributors;
- watchers;
- open issues;
- last push.

## RepositoryScoringService

`RepositoryScoringService` рассчитывает:

- popularity score;
- activity score;
- engagement score;
- demand score.

Значения нормализуются к шкале 0-100.

## KaggleScoreConfigProvider

`KaggleScoreConfigProvider` читает:

```text
data/csv/kaggle/github_repos.csv
```

И на его основе строит `ScoreConfig`:

- saturation thresholds;
- веса для групп score;
- веса итогового demand score.

Для расчета весов используется Spearman correlation: pandas использует его для `method="spearman"`.

## Требуемые колонки CSV

```text
stars
forks
contributors
merged_pull_requests
commits
open_issues
closed_issues
is_archived
is_fork
```

Если какой-то колонки нет, приложение выбросит ошибку при построении score config.

