import asyncio

from infrastructure.github.config import settings
from infrastructure.github.clients.client import GitHubClient
from infrastructure.di.container import AppContainer
from application.queries.queries import GetHistoryQuery


async def main() -> None:
    async with GitHubClient(settings.TOKEN) as github_client:
        container = AppContainer(github_client)

        get_history_use_case = container.get_history_use_case()

        query = GetHistoryQuery(
            url=settings.GITHUB_URL,
            days=settings.DAYS
        )

        history = await get_history_use_case.execute(query)

        print("=== HISTORY ===")
        print(history.model_dump(mode="json"))


if __name__ == "__main__":
    asyncio.run(main())
