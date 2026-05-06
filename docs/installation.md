# Установка и запуск

## Требования

- Python 3.12+
- GitHub Personal Access Token
- Docker и Docker Compose, если нужен контейнерный запуск
- CSV-датасет:

```text
data/csv/kaggle/github_repos.csv
```

## Подготовка `.env`

Создайте `.env`:

```bash
cp .env.example .env
```

Минимально нужно заполнить:

```env
TOKEN=your_github_token
GITHUB_URL=https://github.com/owner/repository
```

## Локальная установка

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

Для установки dev-зависимостей:

```bash
python -m pip install ".[dev]"
```

## Локальный запуск

```bash
python main.py
```

После запуска откройте результат:

```bash
open repository_analytics_dashboard.html
```

На Linux:

```bash
xdg-open repository_analytics_dashboard.html
```

## Запуск через Docker Compose

```bash
docker compose build
docker compose run --rm repository-parser
```

Если менялись зависимости:

```bash
docker compose build --no-cache
docker compose run --rm repository-parser
```

## Запуск через Docker

```bash
docker build -t repository-parser .
docker run --rm --env-file .env -v "$PWD:/app" repository-parser
```


