# Docker и Docker Compose

Этот вариант подходит, если вы хотите запустить проект без ручной настройки
Python-окружения.

## Перед запуском

Создайте `.env`:

```bash
cp .env.example .env
```

Заполните в нем минимум:

```env
TOKEN=your_github_token
GITHUB_URL=https://github.com/owner/repository
```

## Запуск через Docker Compose

Рекомендуемый способ:

```bash
docker compose up --build
```

Или, если нужно запустить приложение один раз и сразу удалить контейнер после
завершения:

```bash
docker compose run --rm repository-parser
```

После запуска откройте результат:

```bash
open repository_analytics_dashboard.html
```

## Запуск через Docker

Если не используете Docker Compose:

```bash
docker build -t repository-parser .
docker run --rm --env-file .env -v "$PWD:/app" repository-parser
```

## После изменения зависимостей

Если изменился `pyproject.toml`, пересоберите образ:

```bash
docker compose build --no-cache
docker compose run --rm repository-parser
```

