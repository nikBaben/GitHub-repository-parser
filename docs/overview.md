# Обзор проекта

Repository Parser анализирует GitHub-репозиторий и формирует интерактивный
дашборд с историческими графиками и аналитическими показателями.

## Назначение

Проект нужен, чтобы по URL GitHub-репозитория получить:

- историю stars;
- историю forks;
- историю pull requests;
- историю merged pull requests;
- историю commits;
- историю issues;
- историю contributors;
- агрегированные количественные метрики;
- скоринг популярности, активности, вовлеченности и итогового спроса;
- HTML-дашборд с графиками.

## Как работает приложение

```text
1. main.py читает настройки из переменных окружения или .env.
2. GitHubClient создается с GitHub token.
3. AppContainer собирает use cases, сервисы, адаптеры и renderer.
4. GetHistoryQuery извлекает owner и repo из GITHUB_URL.
5. HistoryService проверяет локальный JSON-кэш.
6. Если кэш отсутствует или устарел, данные загружаются из GitHub API.
7. История фильтруется по DAYS.
8. CountMetricsService считает агрегированные метрики.
9. RepositoryScoringService рассчитывает score-показатели.
10. RepositoryDashboardMapper готовит view model для дашборда.
11. PlotlyRepositoryDashboardRenderer сохраняет HTML-дашборд.
```

## Результат работы

После успешного запуска создается файл:

```text
repository_analytics_dashboard.html
```

В нем доступны:

- summary репозитория;
- блок analytics;
- переключатель метрик;
- график значений по периодам;
- график накопительного значения.

