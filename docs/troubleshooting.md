# Решение проблем

## Браузер не открывается при запуске в Docker

Это нормально. Код выполняется внутри контейнера, а не на вашей машине.

Откройте HTML-файл вручную:

```bash
open repository_analytics_dashboard.html
```

Если файла нет, проверьте volume в `docker-compose.yml`:

```yaml
volumes:
  - .:/app
```

## `httpx.ConnectError`

Приложение не может подключиться к GitHub API.

Проверьте:

- интернет;
- DNS;
- VPN/proxy;
- Docker network;
- значение `GITHUB_API_URL`.

## `401 Unauthorized`

GitHub token отсутствует, неверный или истек.

Проверьте:

```env
TOKEN=your_github_token
```

## `403 Rate Limit`

GitHub ограничил количество запросов.

Что можно сделать:

- подождать сброса лимита;
- использовать валидный token;
- уменьшить `DAYS`;
- не удалять `data/json`, чтобы использовать кэш.

## Ошибка Kaggle dataset

Проверьте наличие файла:

```text
data/csv/kaggle/github_repos.csv
```

Проверьте, что в CSV есть нужные колонки:

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

