from typing import Any

from infrastructure.github.clients.base import BaseHttpClient
from config import settings
from utils.datetime_utils import parse_dt
from infrastructure.github.queries import (
    ContributorsQuery,
    ForksQuery,
    PullsQuery,
    IssuesQuery,
    StarsQuery, 
    CommitsQuery,
    GitHubPaginatedQuery,
    default_github_headers,
)

class GitHubClient(BaseHttpClient):
    """Асинхронный HTTP-клиент для работы с GitHub REST API."""
    def __init__(self, token: str) -> None:
        super().__init__()

        self._client.headers.update(
            {
                "X-GitHub-Api-Version": settings.GITHUB_API_VERSION,
                "Authorization": f"Bearer {token}",
            }
        )

    async def _paginate(
        self,
        url: str,
        query: GitHubPaginatedQuery,
    ) -> list[dict[str, Any]]:
        """
        Выполняет постраничную загрузку данных из GitHub API.

        Использует параметры пагинации из query, автоматически увеличивает номер
        страницы и собирает результаты в общий список. Если в query переданы
        stop_field и cutoff_dt, дополнительно фильтрует элементы по дате и
        останавливает загрузку, когда данные становятся старше cutoff_dt
        """
        query_params = query.to_params()
        query_params.setdefault("per_page", settings.DEFAULT_PER_PAGE)

        page = 1
        result: list[dict[str, Any]] = []

        while True:
            query_params["page"] = page

            data, _ = await self.get_json(
                url,
                params=query_params,
                headers=query.headers,
            )

            if not data:
                break

            if query.stop_field is not None and query.cutoff_dt is not None:
                filtered_data = [
                    item
                    for item in data
                    if self._is_on_or_after_cutoff(item, query)
                ]
                result.extend(filtered_data)

                last_dt = parse_dt(query.stop_field.extract_from(data[-1]))

                if last_dt is not None and last_dt < query.cutoff_dt:
                    break
            else:
                result.extend(data)

            page += 1

        return result

    def _is_on_or_after_cutoff(
        self,
        item: dict[str, Any],
        query: GitHubPaginatedQuery,
    ) -> bool:
        """
        Проверяет, находится ли элемент на или после даты отсечения.

        Используется при загрузке исторических данных, чтобы оставить только
        элементы, дата которых больше или равна query.cutoff_dt.
        """
        if query.stop_field is None or query.cutoff_dt is None:
            return True

        item_dt = parse_dt(query.stop_field.extract_from(item))

        if item_dt is None:
            return False

        return item_dt >= query.cutoff_dt

    async def get_repository(
        self,
        owner: str,
        repo: str,
        params: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, str]]:
        """Получает основную информацию о GitHub-репозитории."""
        return await self.get_json(
            f"{settings.GITHUB_API_URL}/repos/{owner}/{repo}",
            headers=default_github_headers(),
        )
    
    async def get_stars(
        self,
        owner: str,
        repo: str,
        query: StarsQuery,
    ) -> list[dict[str, Any]]:
        """Получает историю пользователей, поставивших звезду репозиторию."""
        return await self._paginate(
            f"{settings.GITHUB_API_URL}/repos/{owner}/{repo}/stargazers",
            query=query,
        )

    async def get_forks(
        self,
        owner: str,
        repo: str,
        query: ForksQuery,
    ) -> list[dict[str, Any]]:
        """Получает список форков репозитория."""
        return await self._paginate(
            f"{settings.GITHUB_API_URL}/repos/{owner}/{repo}/forks",
            query=query,
        )
    
    async def get_pulls(
        self,
        owner: str,
        repo: str,
        query: PullsQuery,
    ) -> list[dict[str, Any]]:
        """Получает список пуллов репозитория."""
        return await self._paginate(
            f"{settings.GITHUB_API_URL}/repos/{owner}/{repo}/pulls",
            query=query,
        )
    
    async def get_commits(
        self,
        owner: str,
        repo: str,
        query: CommitsQuery,
    ) -> list[dict[str, Any]]:
        """Получает список коммитов репозитория."""
        return await self._paginate(
            f"{settings.GITHUB_API_URL}/repos/{owner}/{repo}/commits",
            query=query,
        )

    async def get_contributors(
        self,
        owner: str,
        repo: str,
        query: ContributorsQuery | None = None,
    ) -> list[dict[str, Any]]:
        """Получает список контрибьюторов репозитория."""
        return await self._paginate(
            f"{settings.GITHUB_API_URL}/repos/{owner}/{repo}/contributors",
            query=query or ContributorsQuery(),
        )

    async def get_issues(
        self,
        owner: str,
        repo: str,
        query: IssuesQuery,
    ) -> list[dict[str, Any]]:
        """ Получает список ишьюсов репозитория."""
        return await self._paginate(
            f"{settings.GITHUB_API_URL}/repos/{owner}/{repo}/issues",
            query=query,
        )
    
